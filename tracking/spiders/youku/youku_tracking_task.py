# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from youku_base import YoukuBase
from datetime import date, datetime
from tracking.util.YoukuUtil import YoukuUtil
from tracking.items import TrackingItem

class YoukuTracking(YoukuBase):
  name = 'youku_tracking_task'

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

  def loadRequest(self, url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_channel))
    return requests

  def loadItems(self, url, topic, release):
    items = []
    itemTracking = YoukuUtil.get_tracking(url, self.target_channel, release)
    items.append(itemTracking)
    return items
