# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from urlparse import urljoin
from iqiyi_base import IqiyiBase
from datetime import date, datetime
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TopicItem, PlaycountItem, ChannelItem

reload(sys)
sys.setdefaultencoding('utf-8')

class IqiyiTracking(IqiyiBase):
  name = 'iqiyi_tracking_task'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302,
    },
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
    },
    'DOWNLOAD_DELAY':0.2,
  }

  def loadRequest(self, channel_url, url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_vid))
    return requests

  def loadItems(self, url, topic, release, playcount, commentCount, upCount, downCount):
    items = []
    itemTracking = BaseUtil.get_tracking(url, self.target_channel, release)
    items.append(itemTracking)
    return items
