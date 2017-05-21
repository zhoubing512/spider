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
from tracking.util.WeiboUtil import WeiboUtil

GENERAL_CODE = "utf-8"

class WeiboHotSearch(Spider):
  name = "weibo_hot_search_task"
  source = "weibo"
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
    "http://s.weibo.com/top/summary?cate=realtimehot",       # 实时热搜
    "http://s.weibo.com/top/summary?cate=total&key=all",     # 热点热搜
    "http://s.weibo.com/top/summary?cate=total&key=films",   # 潮流热搜
    "http://s.weibo.com/top/summary?cate=total&key=person",  # 名人热搜
  ]

  ts = WeiboUtil.date_time_now()

  def start_requests(self):
    for url in self.start_urls:
      yield Request(url, callback=self.parse)

  def parse(self, response):
    print response.url
    print self.identify(response.url)
    script_list = re.findall('<script>STK \&\& STK\.pageletM \&\& STK\.pageletM\.view\((.+)\)<\/script>', response.body)
    html = ""
    for script in script_list:
      hjson = json.loads(script, encoding=GENERAL_CODE)
      if hjson["pid"] == "pl_top_total" or hjson["pid"] == "pl_top_realtimehot":
        html = hjson["html"]
        break
    if html == "":
      return
    selector = Selector(text=html, type="html")
    hover_list = selector.xpath('.//tr[@action-type="hover"]')
    for hover in hover_list:
      ranking = int(hover.xpath('.//td[@class="td_01"]').xpath('string(.)').extract_first())
      keyword = hover.xpath('.//td[@class="td_02"]/div/p/a').xpath('string(.)').extract_first()
      index = int(hover.xpath('.//td[@class="td_03"]').xpath('string(.)').extract_first())
      print ranking, keyword, index, self.ts
      rk = RankingItem()
      rk["rank"] = ranking
      rk["name"] = keyword
      rk["index"] = index
      rk["species"] = self.identify(response.url)
      rk["ts"] = self.ts
      yield rk

  def identify(self, url):
    if "realtimehot" in url:
      return "实时"
    elif "all" in url:
      return "热点"
    elif "films" in url:
      return "潮流"
    elif "person" in url:
      return "人物"
