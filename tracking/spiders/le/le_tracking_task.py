# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from le_base import LeBase
from datetime import date, datetime
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TrackingItem

class LeTracking(LeBase):
  name = 'le_tracking_task'

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

  def loadItems(self, vid, url, topic, release, playcount):
    items = []
    itemTracking = BaseUtil.get_tracking(url, self.target_channel, release)
    items.append(itemTracking)
    return items
