# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import datetime
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import Spider
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, ChannelItem
from tracking.util.MiaopaiUtil import MiaopaiUtil
from tracking.spiders.spider_base import SpiderBase
from tracking.util.BaseUtil import BaseUtil


GENERAL_CODE = "utf-8"

class MiaopaiIndicators(SpiderBase):
  name = "miaopai_indicators_task"
  source = "miaopai"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },

    'DOWNLOAD_DELAY': 0,
    'CONCURRENT_REQUESTS': 60,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 60,
    'CONCURRENT_REQUESTS_PER_IP': 60,
  }

  csr_url = ""

  start_urls = [
  ]

  tracking_user_urls = [
    #"http://www.miaopai.com/u/paike_bdkn4d4b7s",  # 好好吃
  ]


  url_reg_pre = "http://www.miaopai.com/show/"

  url_user_pre = "http://www.miaopai.com/u/"

  url_filter = "http://www.miaopai.com"

  def start_requests(self):
    self.csr_url = self.settings['TRACKING_URL']
    self.tracking_user_urls = self.load_entity()
    for url in self.tracking_user_urls:
      yield Request(url, callback=self.parse_fans)
    yield Request(self.csr_url, callback=self.parse_csr_job)

  def parse_csr_job(self, response):
    print self.static_tags
    print self.target_channel
    hjson = json.loads(response.body)
    for job in hjson["data"]:
      if job["url"] is None:
        continue
      url = MiaopaiUtil.text_clean(job["url"])  #
      tags = job["plan"]["tags"]
      if self.target_channel not in tags:
        continue
      if self.url_reg_pre in job["url"]:
        yield Request(url, callback=self.parse)
      if self.url_user_pre in job["url"]:
        yield Request(url, callback=self.parse_fans)

  def parse(self, response):
    print response.url
    try:
      selector = Selector(text=response.body, type="html")
      id = response.url
      user_name = selector.xpath('.//p[@class="personalDataN"]').xpath('string(.)').extract_first()
      #vid = re.findall('(\w+)\.htm', response.url)[0]
      release_html = selector.xpath('.//p[@class="personalDataT"]/span').xpath('string(.)').extract_first()
      release = MiaopaiUtil.get_miaopai_time(release_html)

      pv = selector.xpath('.//p[@class="personalDataT"]/span[@class="red"]').xpath('string(.)').extract_first()
      pv = int(MiaopaiUtil.convert_playcount(pv))
      video_about = selector.xpath('.//div[@class="viedoAbout"]').xpath('string(.)').extract_first()
      video_about = str(MiaopaiUtil.text_clean(video_about))
      ts = MiaopaiUtil.date_time_now()
      # print id, user_name, release , pv, video_about

      topic = BaseUtil.get_topic(url=id, topic=video_about, channel=self.target_channel, playcount=pv, release=release)
      yield topic
      pc = BaseUtil.get_playcount(url=id, channel=self.target_channel, playcount=pv, release=release)
      yield pc
    except Exception as e:
      print e

  def parse_fans(self, response):
    print response.url
    channel_url = response.xpath('.//p[@class="name"]/a/@href').extract_first()
    name = response.xpath('.//p[@class="name"]/a/span').xpath('string(.)').extract_first()
    name = MiaopaiUtil.text_clean(name)
    fans = response.xpath('.//ul[@class="bottomInfor"]/li[3]/a/span[@class="num"]').xpath('string(.)').extract_first()
    fans = int(MiaopaiUtil.convert_playcount(MiaopaiUtil.text_clean(fans)))

    ch = ChannelItem()
    ch["id"] = channel_url
    ch["fans"] = fans
    ch["name"] = self.target_channel
    ch["ts"] = MiaopaiUtil.date_time_now()
    yield ch

