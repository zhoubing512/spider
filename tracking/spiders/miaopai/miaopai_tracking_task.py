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
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, ChannelItem
from tracking.items import TrackingItem
from tracking.util.MiaopaiUtil import MiaopaiUtil
from tracking.spiders.spider_base import SpiderBase

GENERAL_CODE = "utf-8"

class MiaopaiTracking(SpiderBase):
  name = "miaopai_tracking_task"
  source = "miaopai"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302,
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

  url_filter = "http://www.miaopai.com"

  def start_requests(self):
    self.start_urls = self.load_entity()
    for url in self.start_urls:
      yield Request(url, callback=self.parse_index)

  def parse_index(self, response):
    video_list = response.xpath('.//div[@class="videoCont"]')
    for video in video_list:
      url = video.xpath('.//ul[@class="commentLike"]/li/a/@href').extract_first()
      release_html = video.xpath('.//p[@class="personalDataT"]/span').xpath('string(.)').extract_first()
      release = MiaopaiUtil.get_miaopai_time(release_html)
      user_name = video.xpath('.//p[@class="personalDataN"]').xpath('string(.)').extract_first()
      print url, user_name, self.target_channel, release

      tk = TrackingItem()
      tk["id"] = url
      tk["channel"] = self.target_channel
      tk["release"] = release
      yield tk




