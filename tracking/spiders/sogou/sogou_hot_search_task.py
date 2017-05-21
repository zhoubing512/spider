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

GENERAL_CODE = "utf-8"

class SogouHotSearch(Spider):
  name = "sogou_hot_search_task"
  source = "sogou"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middleware.WeiboCookiesHotSearchMiddleware": 402,
    },

    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS_PER_IP': 1,
  }

  start_urls = [
    "http://top.sogou.com/hot/shishi_1.html",       # 实时
    "http://top.sogou.com/movie/all_1.html",        # 电影
    "http://top.sogou.com/tvplay/all_1.html",       # 电视剧
    "http://top.sogou.com/tvshow/all_1.html",       # 综艺
    "http://top.sogou.com/auto/all_1.html",         # 汽车
    "http://top.sogou.com/people/all_1.html",       # 人物
  ]

  ts = BaseUtil.date_time_now()

  def start_requests(self):
    for url in self.start_urls:
      yield Request(url, callback=self.parse)

  def parse(self, response):
    print response.url
    print self.identify(response.url)
    ranking = 0
    pub_list = response.xpath('.//div[@class="main"]/ul/li')
    species = self.identify(response.url)
    for rank in pub_list:
      ranking += 1
      name = rank.xpath('.//span[@class="s2"]/p[@class="p1"]').xpath('string(.)').extract_first()
      if name is None:
        name = rank.xpath('.//span[@class="s2"]').xpath('string(.)').extract_first()
      index = int(rank.xpath('.//span[@class="s3"]').xpath('string(.)').extract_first())
      rk = RankingItem()
      rk["rank"] = ranking
      rk["name"] = name
      rk["index"] = index
      rk["species"] = species
      rk["ts"] = self.ts
      yield rk

  def identify(self, url):
    if "people" in url:
      return "人物"
    elif "auto" in url:
      return "汽车"
    elif "movie" in url:
      return "影视"
    elif "tvplay" in url:
      return "电视剧"
    elif "tvshow" in url:
      return "综艺"
    return "综合"
