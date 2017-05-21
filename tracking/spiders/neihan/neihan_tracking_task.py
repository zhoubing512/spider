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
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, RepostItem, DurationItem, ChannelItem
from tracking.items import UpCountItem, DownCountItem, CollectionCountItem
from tracking.items import TrackingItem
from tracking.util.NeihanUtil import NeihanUtil
from neihan_base import NeihanBase

GENERAL_CODE = "utf-8"


class NeihanTracking(NeihanBase):
  name = "neihan_tracking_task"
  source = "neihan"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },

    'DOWNLOAD_DELAY': 0.5,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS_PER_IP': 1,
  }

  def start_requests(self):

    for user in self.start_urls:
      uid = re.findall('\d+', user)[0]
      url = self.generate_url(uid, 0, 20)
      yield Request(url=url, callback=self.parse)



  def parse(self, response):
    print response.url
    hjson = json.loads(response.body.encode(GENERAL_CODE))
    ts = NeihanUtil.date_time_now()
    for data in hjson["data"]["data"]:
      if int(data["media_type"]) != 3:  # 不是视频还抓个毛
        continue
      res = self.parse_data(data)
      if res is None:
        continue
      (detail_url, text, user_name, create_time, comment_count, share_count, digg_count, bury_count, favorite_count) = res

      tk = TrackingItem()
      tk["id"] = detail_url
      tk["channel"] = user_name
      tk["release"] = create_time
      yield tk

    hasmore = int(hjson["data"]["hasmore"])
    if hasmore > 0:
      options = hjson["data"]["options"]
      count = options["count"]
      page = options["page"]
      user_id = hjson["user_id"]
      next_page = self.generate_url(user_id, page, count)
      yield Request(url=next_page, callback=self.parse)

