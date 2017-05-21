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
from tracking.items import TrackingItem
from tracking.util.MiaopaiUtil import MiaopaiUtil
from tracking.spiders.spider_base import SpiderBase

GENERAL_CODE = "utf-8"

class MiaopaiIndicators(SpiderBase):
  name = "miaopai_repayment"
  source = "miaopai"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },

    'DOWNLOAD_DELAY': 0,
    'CONCURRENT_REQUESTS': 60,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 60,
    'CONCURRENT_REQUESTS_PER_IP': 60,
  }


  start_urls = [
  ]

  target_channel = ""

  static_tags = [""]

  url_reg_pre = "http://www.miaopai.com/show/"

  url_user_pre = "http://www.miaopai.com/u/"

  url_filter = "http://www.miaopai.com"

  def start_requests(self):
    for url in self.start_urls:
      yield Request(url=url, callback=self.parse)

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

      tk = TrackingItem()
      tk["id"] = response.url
      tk["channel"] = user_name
      tk["release"] = release
      yield tk

    except Exception as e:
      print e

