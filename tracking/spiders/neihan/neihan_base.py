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
from tracking.spiders.spider_base import SpiderBase
from tracking.util.NeihanUtil import NeihanUtil

GENERAL_CODE = "utf-8"

class NeihanBase(SpiderBase):
  name = "neihan_base"
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

  # TODO: 从ES获取Channel ?
  start_urls = [
    "http://neihanshequ.com/user/6009077444/"
  ]

  fans_url = "http://lf.snssdk.com/neihan/user/profile/v2/?device_type=iPhone%%206S&version_code=6.1.8&ac=WIFI&screen_width=750&aid=7&user_id=%s"

  base_url = "http://neihanshequ.com/user/%s//?is_json=1&page=%s&count=%s"

  url_filter = "neihanshequ.com"

  def parse_data(self, data):
    text = NeihanUtil.text_clean(data["text"])
    #user_name = NeihanUtil.text_clean(data["user"]["name"])
    user_name = self.target_channel
    uid = data["user"]["user_id"]
    did = str(data["detail_url"])
    detail_url = self.get_detial_url(did)
    create_time = int(data["create_time"])
    go_detail_count = int(data["go_detail_count"])

    digg_count = int(data["digg_count"])  # 赞
    bury_count = int(data["bury_count"])  # 踩
    favorite_count = int(data["favorite_count"])  # 爱
    comment_count = int(data["comment_count"])  # 评
    share_count = int(data["share_count"])  # 转
    return detail_url, text, user_name, create_time, comment_count, share_count, digg_count, bury_count, favorite_count

  def generate_url(self, uid, page, count):
    return self.base_url % (uid, page, count)

  def get_user_url(self, uid):
    return "http://neihanshequ.com/user/%s" % str(uid)

  def get_detial_url(self, did):
    return "http://neihanshequ.com%s" % str(did)
