# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from datetime import date, datetime
from toutiao_base import ToutiaoBase
from tracking.items import TrackingItem
from tracking.util.ToutiaoUtil import ToutiaoUtil

reload(sys)
sys.setdefaultencoding('utf-8')

class ToutiaoTracking(ToutiaoBase):
  name = 'toutiao_tracking_task'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302
    }
  }

  def loadRequest(self, channel_url, url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_channel))
    return requests

  def loadItems(self, url, topic, release, playcount, commentCount, pageView, repostCount, recommendationCount, category):
    items = []
    itemTracking = ToutiaoUtil.get_tracking(url, self.target_channel, release)
    items.append(itemTracking)
    return items
