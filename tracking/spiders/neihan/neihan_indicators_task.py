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
from tracking.util.BaseUtil import BaseUtil

GENERAL_CODE = "utf-8"


class NeihanIndicators(NeihanBase):
  name = "neihan_indicators_task"
  source = "neihan"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
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
    self.start_urls = self.load_entity()
    for user in self.start_urls:
      uid = re.findall('\d+', user)[0]
      url = self.generate_url(uid, 0, 20)
      yield Request(url=url, callback=self.parse)
      yield Request(url=self.fans_url % uid, callback=self.parse_fans)

  def parse_fans(self, response):
    print response.url
    print response.body
    hjson = json.loads(response.body)
    name = hjson["data"]["name"]
    fans = int(hjson["data"]["followers"])
    ch = ChannelItem()
    ch["id"] = response.url
    ch["fans"] = fans
    ch["name"] = self.target_channel
    ch["ts"] = NeihanUtil.date_time_now()
    yield ch

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

      topic = BaseUtil.get_topic(url=detail_url, topic=text, channel=user_name, playcount=data["play_count"], release=create_time)
      yield topic

      pc = BaseUtil.get_playcount(url=detail_url, channel=user_name, playcount=data["play_count"], release=create_time)
      yield pc

      cmc = BaseUtil.get_commentscount(url=detail_url, channel=user_name, count=comment_count)
      yield cmc

      rp = RepostItem()
      rp["id"] = detail_url
      rp["repostCount"] = share_count
      rp["ts"] = ts
      rp["category"] = "video"
      yield rp

      up = UpCountItem()
      up["id"] = detail_url
      up["count"] = digg_count
      up["ts"] = ts
      up["category"] = "video"
      yield up

      down = DownCountItem()
      down["id"] = detail_url
      down["count"] = bury_count
      down["ts"] = ts
      down["category"] = "video"
      yield down

      col = CollectionCountItem()
      col["id"] = detail_url
      col["count"] = favorite_count
      col["ts"] = ts
      col["category"] = "video"
      yield col

      dur = DurationItem()
      dur["id"] = detail_url
      dur["duration"] = data["duration"]
      dur["ts"] = ts
      dur["category"] = "video"
      yield dur

    hasmore = int(hjson["data"]["hasmore"])
    if hasmore > 0:
      options = hjson["data"]["options"]
      count = options["count"]
      page = options["page"]
      user_id = hjson["user_id"]
      next_page = self.generate_url(user_id, page, count)
      yield Request(url=next_page, callback=self.parse)

