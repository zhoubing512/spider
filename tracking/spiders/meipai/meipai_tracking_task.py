# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import datetime
import scrapy
from scrapy import Selector
from urlparse import urljoin
from scrapy.http import Request
from scrapy.spiders import Spider
from meipai_base import MeipaiBase
from tracking.items import TrackingItem
from tracking.util.BaseUtil import BaseUtil

GENERAL_CODE = "utf-8"

class MeipaiTracking(MeipaiBase):
  name = "meipai_tracking_task"
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

  def loadRequest(self, url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_url))
    return requests

  def loadItems(self, url, topic, playcount, release, repost, commentcount, upcount):
    items = []
    itemTracking = BaseUtil.get_tracking(url, self.target_channel,release)
    items.append(itemTracking)
    return items
