# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from scrapy.http import Request
from datetime import date, datetime
from bilibili_base import BilibiliBase
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TopicItem, PlaycountItem, CommentsCountItem, PageviewItem, RepostItem, RecommendationItem, ChannelItem

reload(sys)
sys.setdefaultencoding('utf-8')

class BilibiliIndicators(BilibiliBase):
  name = 'bilibili_tracking_task'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302,
    }
  }

  def loadRequest(self, uid ,url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_channel))
    return requests

  def loadItems(self, url, topic, release, playcount, commentCount):
    items = []
    itemTracking = BaseUtil.get_tracking(url, self.target_channel, release)
    items.append(itemTracking)
    return items
