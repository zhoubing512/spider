# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from urlparse import urljoin
from datetime import date, datetime
from netease_base import NeteaseBase
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TopicItem, PlaycountItem, ChannelItem
reload(sys)
sys.setdefaultencoding('utf-8')

class NeteaseIndicators(NeteaseBase):
  name = 'netease_indicators_task'
  base_playcount_url = 'http://dy.163.com/wemedia/datacenter/video/pv/view.do?wemediaId=%s'
  article_playcount_url = 'http://dy.163.com/wemedia/datacenter/article/pv/view.do?wemediaId=%s'
  channel_fans_url = 'http://dy.163.com/wemedia/general.json?wemediaId=%s'
  channel_home_url = 'http://dy.163.com/wemedia/notice/list/1/20.html?wemediaId=%s'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middlewareCookie.CookieMiddleware": 402,
    },
    'DOWNLOAD_DELAY':0.2,
  }

  def loadRequests(self, uid):
    requests = []
    requests.append(scrapy.Request(self.channel_fans_url % uid, callback=self.parse_fans, meta={'uid':uid}))
    requests.append(scrapy.Request(self.base_playcount_url % uid, callback=self.parse_playcount, meta={'uid': uid, 'category': BaseUtil.Category.VIDEO}))
    requests.append(scrapy.Request(self.article_playcount_url % uid, callback=self.parse_playcount, meta={'uid': uid, 'category': BaseUtil.Category.ARTICLE}))
    return requests

  def parse_playcount(self, response):
    uid = response.meta['uid']
    category = response.meta['category']
    url = self.base_user_home % uid
    topic='all videos'
    if category == BaseUtil.Category.VIDEO:
      topic='all videos'
      url = self.base_user_home % uid
    elif category == BaseUtil.Category.ARTICLE:
      topic='all articles'
      url = self.base_user_article_home % uid
    jsonObj = json.loads(response.body_as_unicode())
    if 'data' in jsonObj.keys() and 'total' in jsonObj['data'].keys():
      release = BaseUtil.date_time_now()
      playcount = int(jsonObj['data']['total'])
      itemTopic = BaseUtil.get_topic(url=url, topic=topic, channel=self.target_channel, playcount=playcount, release=release, category=category)
      yield itemTopic
      itemPlaycount = BaseUtil.get_playcount(url=url, channel=self.target_channel, playcount=playcount, release=release, category=category)
      yield itemPlaycount

  def parse_fans(self, response):
    fansJson = json.loads(response.body_as_unicode())
    fansCount = 0
    if 'data' in fansJson.keys() and 'sumSubs' in fansJson['data'].keys():
      fansCount = int(fansJson['data']['sumSubs'])
    item = BaseUtil.get_channel(url=self.channel_home_url % response.meta['uid'], name=self.target_channel, fans=fansCount)
    yield item
