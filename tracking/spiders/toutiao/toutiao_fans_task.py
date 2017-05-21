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
from tracking.util.ToutiaoUtil import ToutiaoUtil
from tracking.items import TopicItem, PlaycountItem, CommentsCountItem, PageviewItem, RepostItem, RecommendationItem, ChannelItem

reload(sys)
sys.setdefaultencoding('utf-8')

class ToutiaoFans(ToutiaoBase):
  name = 'toutiao_fans_task'

  custom_settings = {
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.ProxyMiddleware": 401,
    },
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'CONCURRENT_REQUESTS_PER_IP': 5
  }

  def loadRequest(self, channel_url, url):
    requests = []
    requests.append(scrapy.Request(channel_url, callback=self.parse_fans))
    return requests

  def parse_fans(self, response):
    fansCount = 0
    fansObj = re.search("fensi:'(\d+)'", response.body)
    if fansObj is not None:
      fansCount = int(fansObj.group(1))
    itemFans = ToutiaoUtil.get_channel(response.url, self.target_channel, fansCount)
    yield itemFans
