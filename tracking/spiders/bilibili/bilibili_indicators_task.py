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
  name = 'bilibili_indicators_task'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    }
  }

  def loadRequest(self, uid ,url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_channel))
    requests.append(scrapy.Request(self.meta_url % uid, callback=self.parse_fans, meta={'uid':uid}))
    return requests

  def loadItems(self, url, topic, release, playcount, commentCount):
    items = []
    channel = self.target_channel
    itemTopic = BaseUtil.get_topic(url, topic, channel, playcount, release)
    items.append(itemTopic)
    itemPlaycount = BaseUtil.get_playcount(url, channel, playcount, release)
    items.append(itemPlaycount)
    itemCommentCount = BaseUtil.get_commentscount(url,channel,commentCount)
    items.append(itemCommentCount)
    return items

  def parse_fans(self, response):
    jsonObj = json.loads(response.body_as_unicode())
    if 'data' in jsonObj.keys():
      fansObj = jsonObj['data']
      fansCount = 0
      if 'results' in fansObj.keys():
        fansCount = int(fansObj['results'])
      url = self.base_user_url % response.meta['uid']
      itemFans = BaseUtil.get_channel(url, self.target_channel, fansCount)
      yield itemFans
