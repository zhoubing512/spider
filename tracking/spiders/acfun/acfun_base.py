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
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, RankingItem
from tracking.util.BaseUtil import BaseUtil
from tracking.util.TrackingUtil import TrackingUtil
from tracking.spiders.spider_base import SpiderBase

GENERAL_CODE = "utf-8"

class AcfunBase(SpiderBase):
  name = "acfun_base"
  source = "acfun"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },

    'DOWNLOAD_DELAY': 0,
    'CONCURRENT_REQUESTS': 16,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    'CONCURRENT_REQUESTS_PER_IP': 16,
  }


  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  start_urls = [
    "http://www.acfun.cn/u/9400024.aspx"
  ]

  url_filter = "http://www.acfun.cn/"

  user_url_base = "http://www.acfun.cn/u/%s.aspx"
  list_url_base = "http://www.acfun.cn/space/next?uid=%s&type=video&orderBy=2&pageNo=%s"
  av_url_base = "http://www.acfun.cn%s"
  av_url_base_s = "http://www.acfun.cn/v/ac%s"

  def start_requests(self):
    self.start_urls = self.load_entity()
    for url in self.start_urls:
      yield Request(url=url, callback=self.parse_fans)

  def parse_fans(self, response):
    print response.url
    fans = int(re.findall('<span class="fl fans">(\d+)<\/span>', response.body)[0])
    ch = BaseUtil.get_channel(url=response.url, name=self.target_channel, fans=fans)
    yield ch
    uid = re.findall('\/u\/(\d+)', response.url)[0]
    url = self.generate_list_url(uid, 1)
    yield Request(url, callback=self.parse_list)

  def parse_list(self, response):
    print response.url
    uid = str(re.findall('uid=(\d+)', response.url)[0])
    hjson = json.loads(response.body, encoding=GENERAL_CODE)
    html = hjson["data"]["html"]
    selector = Selector(text=html, type="html")
    av_list = selector.xpath('.//a[@target="_blank"]')
    for av_info in av_list:
      av_id = av_info.xpath('@href').extract_first()
      url = self.generate_av_url(av_id)
      # name = self.name_map[uid]
      name = self.target_channel  # use entity name instead of the name from page
      topic = BaseUtil.text_clean(av_info.xpath('.//figure/@data-title').extract_first())
      view = int(av_info.xpath('.//span[@class="view"]/span[@class="nums"]').xpath('string(.)').extract_first())
      release = av_info.xpath('.//img/@src').extract_first()
      release = int(re.findall('http:\/\/imgs\.aixifan\.com\/content\/\d{4}_\d{2}_\d{2}\/(\d+)\.', release)[0])
      print url, name, view, topic, release
      res = self.parse_av_list(av_id, url, name, topic, view, release)
      for item in res:
        yield item

    pageNo = int(hjson["data"]["page"]["pageNo"])
    totalPage = int(hjson["data"]["page"]["totalPage"])
    if pageNo < totalPage:
      next_url = self.generate_list_url(uid, pageNo + 1)
      yield Request(next_url, callback=self.parse_list)

  def parse_av_list(self, av_id, url, name, topic, view, release):
    raise NotImplementedError()

  def generate_list_url(self, uid, page):
    return self.list_url_base % (uid, page)

  def generate_av_url(self, avid):
    return self.av_url_base % avid

