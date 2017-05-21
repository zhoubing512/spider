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

class AutohomeBase(SpiderBase):
  name = "autohome_base"
  source = "autohome"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },

    'DOWNLOAD_DELAY': 0.1,
    'CONCURRENT_REQUESTS': 16,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    'CONCURRENT_REQUESTS_PER_IP': 16,
  }


  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  start_urls = [
  ]

  url_filter = "youchuang.autohome.com.cn/"

  list_base = "http://youchuang.autohome.com.cn/Authors/%s?InfoType=0&page=%s&pagesize=%s"

  topic_base = "http://youchuang.autohome.com.cn/info/%s"

  def start_requests(self):
    self.start_urls = self.load_entity()
    for url in self.start_urls:
      uid = re.findall("Authors/(\d+)", url)[0]
      url = self.generate_list_url(uid, 1)
      yield Request(url=url, callback=self.parse_user, dont_filter=True)
      yield Request(url=url, callback=self.parse_list, dont_filter=True)

  def parse_user(self, response):
    pass

  def parse_list(self, response):
    print response.url
    waterfall_list = response.xpath('.//ul[@class="waterfall-list"]/li/div[@class="waterfall"]')
    for waterfall in waterfall_list:
      waterfall_type = waterfall.xpath('.//div[@class="waterfall-prompt"]/font').xpath('string(.)').extract_first()
      category = BaseUtil.Category.VIDEO
      if "文" in str(waterfall_type):
        category = BaseUtil.Category.ARTICLE
      release = waterfall.xpath('.//div[@class="waterfall-prompt"]/span').xpath('string(.)').extract_first()
      release = int(time.mktime(time.strptime(release, '%Y-%m-%d')))
      url_info = waterfall.xpath('.//div[@class="waterfall-link"]/a/@href').extract_first()
      tid = re.findall("info/(\d+)", url_info)[0]
      url = self.generate_topic_url(tid)
      name = self.target_channel

      waterfall_set = waterfall.xpath('.//div[@class="waterfall-sets"]')
      play_count = waterfall_set.xpath('.//i[@class="sets-view"]/..').xpath('string(.)').extract_first()
      play_count = BaseUtil.convert_playcount(play_count)
      cmc = waterfall_set.xpath('.//span[@class="fn-txt-center"]').xpath('string(.)').extract_first()
      title = waterfall.xpath('.//div[@class="waterfall-link"]/p').xpath('string(.)').extract_first()
      lst = self.parse_item(url, name, release, play_count, cmc, title, category)
      for item in lst:
        yield item
    if len(waterfall_list) > 0:
      this_page = int(re.findall('page=(\d+)', response.url)[0])
      uid = re.findall("Authors/(\d+)", response.url)[0]
      next_url = self.generate_list_url(uid, this_page + 1)
      yield Request(url=next_url, callback=self.parse_list, dont_filter=True)

  def parse_item(self, url, name, release, play_count, cmc, title, category):
    raise NotImplementedError

  def generate_list_url(self, uid, page):
    return self.list_base % (uid, page, 20)

  def generate_topic_url(self, tid):
    return self.topic_base % tid
