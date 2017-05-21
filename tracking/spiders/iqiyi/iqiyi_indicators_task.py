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

class IqiyiIndicators(IqiyiBase):
  name = 'iqiyi_indicators_task'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
    },
    'DOWNLOAD_DELAY':0.2,
  }

  def loadRequest(self, channel_url, url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_vid))
    requests.append(scrapy.Request(channel_url, callback=self.parse_fans, dont_filter=True))
    return requests

  def loadItems(self, url, topic, release, playcount, commentCount, upCount, downCount):
    items = []
    channel = self.target_channel
    itemTopic = BaseUtil.get_topic(url, topic, channel, playcount, release)
    items.append(itemTopic)
    itemPlaycount = BaseUtil.get_playcount(url, channel, playcount, release)
    items.append(itemPlaycount)
    itemCommentCount = BaseUtil.get_commentscount(url,channel,commentCount)
    items.append(itemCommentCount)
    itemUp = BaseUtil.get_upCount(url, upCount)
    items.append(itemUp)
    itemDown = BaseUtil.get_downCount(url, downCount)
    items.append(itemDown)
    return items

  def parse_fans(self, response):
    fans = 0
    fansObj = response.xpath('//a[@data-fans="fans"]/@data-countnum').extract_first()
    if fansObj is not None:
      fans = int(fansObj)
      item = BaseUtil.get_channel(response.url, self.target_channel, fans)
      yield item
