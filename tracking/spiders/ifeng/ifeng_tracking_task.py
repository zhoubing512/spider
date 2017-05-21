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
from ifeng_base import IfengBase

GENERAL_CODE = "utf-8"

class IfengTracking(IfengBase):
  name = "ifeng_tracking_task"
  source = "ifeng"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineMonitor.MonitorPipeline': 302,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middlewareCookie.CookieMiddleware": 402,
    },

    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS_PER_IP': 1,
  }


  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  def start_requests(self):
    url = self.generate_url(self.target_uid, 1)
    yield Request(url, callback=self.parse)

  def parse(self, response):
    print response.url
    hjson = json.loads(response.body, encoding=GENERAL_CODE)
    rows = hjson["data"]["rows"]
    for video in rows:
      url, playcount, commentcount, topic, release = self.parse_video(video)
      tk = BaseUtil.get_tracking(url=url, channel=self.target_name, release=release)
      yield tk

    total = int(hjson["data"]["total"])
    this_page = int(re.findall('pageNumber=(\d+)', response.url)[0])
    if total > self.page_size * this_page:
      next_url = self.generate_url(self.target_uid, page=this_page + 1)
      yield Request(next_url, callback=self.parse)
