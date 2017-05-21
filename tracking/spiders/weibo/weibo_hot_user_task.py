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
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, BigVItem
from tracking.util.WeiboUtil import WeiboUtil

GENERAL_CODE = "utf-8"

class WeiboHotUser(Spider):
  name = "weibo_hot_user_task"
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
    "http://v6.bang.weibo.com/czv/qiche?luicode=40000050",       # 汽车
    "http://v6.bang.weibo.com/czv/yule?luicode=40000050",        # 娱乐
    "http://v6.bang.weibo.com/czv/tiyu?luicode=40000050",        # 体育
    "http://v6.bang.weibo.com/czv/dianying?luicode=40000050",    # 电影
    "http://v6.bang.weibo.com/czv/dianshiju?luicode=40000050",   # 电视剧
    "http://v6.bang.weibo.com/czv/zongyi?luicode=40000050",      # 综艺
  ]

  ts = WeiboUtil.date_time_now()
  user_url = "http://weibo.com/u/%s"

  def start_requests(self):
    for url in self.start_urls:
      yield Request(url, callback=self.parse)

  def parse(self, response):
    print response.url
    script_list = re.findall('<script>FM.view\((.+)\)<\/script>', response.body)
    data = ""
    for script in script_list:
      hjson = json.loads(script, encoding=GENERAL_CODE)
      if hjson["ns"] == "mpl.listUserCzv.index":
        data = hjson["data"]
        break
    if data == "":
      return
    data = json.loads(json.dumps(data))
    #data_json = json.dumps(data, encoding=GENERAL_CODE)
    #print data_json
    rank = 0
    for obj in data["list_data"]:
      rank += 1
      user_name = obj["screen_name"]
      user_url = self.user_url % obj["uid"]
      index = float(obj["score"])
      species = self.identify(response.url)
      print rank, user_url, user_name, index, species

      rk = BigVItem()
      rk["rank"] = rank
      rk["name"] = user_name
      rk["index"] = index
      rk["species"] = species
      rk["ts"] = self.ts
      yield rk

  def identify(self, url):
    if "qiche" in url:
      return "汽车"
    elif "yule" in url:
      return "娱乐"
    elif "tiyu" in url:
      return "体育"
    elif "dianying" in url or "dianshiju" in url or "zongyi" in url:
      return "影视"
    return "综合"
