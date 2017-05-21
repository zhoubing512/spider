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

class YidianzixunBase(SpiderBase):
  name = "yidianzixun_base"
  source = "yidianzixun"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middlewareCookie.CookieMiddleware": 402,
    },

    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 16,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    'CONCURRENT_REQUESTS_PER_IP': 16,
  }


  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  start_urls = [
  ]

  url_filter = "yidianzixun.com"

  user_url_base = "http://mp.yidianzixun.com/api/users/get-homepage-data"
  list_url_base = "http://mp.yidianzixun.com/model/Article?page=1&page_size=1000&status=2%2C7&has_data=1&type=original&from_time=&to_time=&title="
  videl_url_base = "http://www.yidianzixun.com/article/%s"

  def start_requests(self):
    self.start_urls = self.load_entity()
    yield Request(url=self.user_url_base, callback=self.parse_user)
    yield Request(url=self.list_url_base, callback=self.parse_list)

  def parse_user(self, response):
    pass

  def parse_list(self, response):
    print response.url
    hjson = json.loads(response.body, encoding=GENERAL_CODE)
    for video in hjson["posts"]:
      name = self.target_channel
      url = self.videl_url_base % video["news_id"]
      title = video["title"]
      release = int(video["date"]) / 1000
      play_count = int(video["data"]["clickDoc"])
      recommendation = int(video["data"]["viewDoc"])
      cmc = int(video["data"]["addCommentDoc"])
      # print url, name, play_count, recommendation, release, title
      res = self.parse_item(url, name, play_count, recommendation, cmc, release, title)
      for item in res:
        yield item

  def parse_item(self, url, name, play_count, recommendation, cmc, release, title):
    raise NotImplementedError
