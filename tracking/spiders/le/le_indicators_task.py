# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from urlparse import urljoin
from le_base import LeBase
from datetime import date, datetime
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TopicItem, PlaycountItem, ChannelItem

reload(sys)
sys.setdefaultencoding('utf-8')

class LeIndicators(LeBase):
  name = 'le_indicators_task'
  base_comment_url = 'http://api.my.le.com/vcm/api/list?cid=30&type=video&page=1&xid=%s&pid=10033959&listType=1'

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

  def loadItems(self, vid, url, topic, release, playcount):
    items = []
    channel = self.target_channel
    if vid != '':
      items.append(scrapy.Request(self.base_comment_url % vid, callback=self.parse_comment_count, meta={'url':url}))
    itemTopic = BaseUtil.get_topic(url, topic, channel, playcount, release)
    items.append(itemTopic)
    itemPlaycount = BaseUtil.get_playcount(url, channel, playcount, release)
    items.append(itemPlaycount)
    return items

  def parse_comment_count(self, response):
    jsonObj = json.loads(response.body_as_unicode())
    if 'total' in jsonObj.keys():
      cmtCount = int(jsonObj['total'])
      item = BaseUtil.get_commentscount(response.meta['url'],self.target_channel,cmtCount)
      yield item
