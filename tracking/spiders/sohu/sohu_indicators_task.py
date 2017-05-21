# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from sohu_base import SohuBase
from datetime import date, datetime
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TopicItem, PlaycountItem, CommentsCountItem, PageviewItem, RepostItem, RecommendationItem, ChannelItem

class SohuIndicators(SohuBase):
  name = 'sohu_indicators_task'
  base_playcount_url = 'http://vstat.v.blog.sohu.com/dostat.do?method=getVideoPlayCount&v=%s&n=bvid'
  base_like_url = 'http://score.my.tv.sohu.com/digg/get.do?vid=%s&type=9001'
  base_fans_url = 'http://push.my.tv.sohu.com/user/a/fo/batchJudge.do?uids=%s'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
    },
    'DOWNLOAD_DELAY':0.2
  }

  def loadRequests(self, uid, channel_url):
    requests = []
    requests.append(scrapy.Request(self.base_scan_url % (uid, '1'), callback=self.parse_channel, meta={'uid': uid}))
    requests.append(scrapy.Request(self.base_fans_url % uid, callback=self.parse_fans, meta={'uid': uid, 'channel_url':channel_url}))
    return requests

  def loadItems(self, vid, url, topic, release):
    items = []
    items.append(scrapy.Request(self.base_playcount_url % vid, callback=self.parse_topic, meta={'url':url, 'release':release, 'topic':topic}))
    items.append(scrapy.Request(self.base_like_url % vid, callback=self.parse_like, meta={'url':url}))
    return items

  def parse_topic(self, response):
    body = response.body_as_unicode()
    jsonStr = body[body.find('bvid=[')+6:-2]
    playcount = 0
    url = response.meta['url']
    topic = response.meta['topic']
    release = response.meta['release']
    channel = self.target_channel
    if jsonStr is not None:
      jsonObj = json.loads(jsonStr)
      if 'count' in jsonObj.keys():
        playcount = jsonObj['count']
    itemTopic = BaseUtil.get_topic(url, topic, channel, playcount, release)
    itemPlaycount = BaseUtil.get_playcount(url, channel, playcount, release)
    yield itemTopic
    yield itemPlaycount

  def parse_like(self, response):
    body = BaseUtil.json_clean(response.body_as_unicode())
    jsonStr = body[2:-2]
    upCount = 0
    downCount = 0
    jsonObj = json.loads(jsonStr)
    url = response.meta['url']
    if jsonObj is not None:
      if 'upCount' in jsonObj.keys():
        upCount = int(jsonObj['upCount'])
      if 'downCount' in jsonObj.keys():
        downCount = int(jsonObj['downCount'])
    itemUp = BaseUtil.get_upCount(url, upCount)
    itemDown = BaseUtil.get_downCount(url, downCount)
    yield itemUp
    yield itemDown

  def parse_fans(self, response):
    jsonObj = json.loads(response.body_as_unicode())
    fansCount = 0
    if 'fansCount' in jsonObj.keys():
      fansCount = int(jsonObj['fansCount'][0])
    item = BaseUtil.get_channel(response.meta['channel_url'], self.target_channel, fansCount)
    yield item
