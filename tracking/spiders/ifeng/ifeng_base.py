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
from tracking.spiders.spider_base import SpiderBase

GENERAL_CODE = "utf-8"

class IfengBase(SpiderBase):
  name = "ifeng_base"
  source = "ifeng"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },

    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS_PER_IP': 1,
  }

  start_urls = [

  ]

  url_pre = "http://fhh.ifeng.com/api/video/videoList?operationStatus=0&pageSize=%s&pageNumber=%s&_=%s"
  fans_url = "http://fhh.ifeng.com/api/homePage/homePageData"
  target_uid = "1492586598136"
  target_name = "好好吃"
  page_size = 30

  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  def start_requests(self):
    url = self.generate_url(self.target_uid, 1)
    yield Request(url, callback=self.parse)

  def parse_video(self, video):
    url = video["pcUrl"]
    playcount = video["pv"]
    commentcount = video["commentNum"]
    topic = video["title"]
    r = re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', video["submitAuditTime"])
    if len(r) > 0:
      release = int(time.mktime(time.strptime(video["submitAuditTime"], '%Y-%m-%d %H:%M:%S')))
    else:
      release = 0
    return url, playcount, commentcount, topic, release

  def generate_url(self, uid, page):
    return self.url_pre % (self.page_size, page, uid)
