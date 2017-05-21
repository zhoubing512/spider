# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from sohu_base import SohuBase
from datetime import date, datetime
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TrackingItem

class SohuTracking(SohuBase):
  name = 'sohu_tracking_task'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302,
    },
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
    },
    'DOWNLOAD_DELAY':0.2
  }

  def loadRequests(self, uid, channel_url):
    requests = []
    requests.append(scrapy.Request(self.base_scan_url % (uid, '1'), callback=self.parse_channel, meta={'uid': uid}))
    return requests

  def loadItems(self, vid, url, topic, release):
    items = []
    itemTracking = BaseUtil.get_tracking(url, self.target_channel, release)
    items.append(itemTracking)
    return items
