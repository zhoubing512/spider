# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from urlparse import urljoin
from uc_base import UcBase
from datetime import date, datetime
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TopicItem, PlaycountItem, ChannelItem

reload(sys)
sys.setdefaultencoding('utf-8')

class UcTracking(UcBase):
  name = 'uc_tracking_task'

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

  def loadItems(self, url, topic, release, playcount, commentCount, pageViewCount, repostCount):
    items = []
    itemTracking = BaseUtil.get_tracking(url, self.target_channel, release)
    items.append(itemTracking)
    return items
