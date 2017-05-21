# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from urlparse import urljoin
from youku_base import YoukuBase
from datetime import date, datetime
from tracking.util.YoukuUtil import YoukuUtil
from tracking.items import TopicItem, PlaycountItem, ChannelItem

reload(sys)
sys.setdefaultencoding('utf-8')

class YoukuIndicators(YoukuBase):
  name = 'youku_indicators_task'
  base_playcount_url = 'http://v.youku.com/action/getVideoPlayInfo?vid=%s&param%%5B%%5D=updown&callback=tuijsonp3'

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

  def loadRequest(self, url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_channel))
    requests.append(scrapy.Request(url, callback=self.parse_fans, dont_filter=True))
    return requests

  def loadItems(self, url, topic, release):
    items = []
    items.append(scrapy.Request(url, callback=self.parse_vid, meta={'topic':topic,'release':release}))
    return items

  def parse_fans(self, response):
    url = response.xpath('//a[@class="username"]/@href').extract_first()
    url = urljoin(self.base_user_url, url)
    fans = int(response.xpath('//li[@class="snum"]/@title').extract_first())
    itemFans = YoukuUtil.get_channel(url, self.target_channel, fans)
    yield itemFans

  def parse_vid(self, response):
    vidObj = re.search('videoId:"(\d+)"', response.body_as_unicode())
    if vidObj is not None:
      yield scrapy.Request(self.base_playcount_url % vidObj.group(1), callback=self.parse_playcount, meta={'url':response.url,'topic':response.meta['topic'],'release':response.meta['release']})

  def parse_playcount(self, response):
    url = response.meta['url']
    topic = response.meta['topic']
    channel = self.target_channel
    release = response.meta['release']
    jsonstr = re.search('tuijsonp3\((.*)\)', response.body_as_unicode())
    inforj = json.loads(jsonstr.group(1))
    if inforj is not None:
      up = 0
      down = 0
      playcount = 0
      if 'data' in inforj.keys():
        if 'updown' in inforj['data'].keys():
          if 'up' in inforj['data']['updown'].keys():
            up = int(inforj['data']['updown']['up'].replace(',', ''))
          if 'down' in inforj['data']['updown'].keys():
            down = int(inforj['data']['updown']['down'].replace(',', ''))
        if 'stat' in inforj['data'].keys() and 'vv' in inforj['data']['stat'].keys():
          playcount = int(inforj['data']['stat']['vv'].replace(',', ''))
      itemTopic = YoukuUtil.get_topic(url, topic, channel, playcount, release)
      yield itemTopic
      itemPlaycount = YoukuUtil.get_playcount(url, channel, playcount, release)
      yield itemPlaycount
      itemUp = YoukuUtil.get_upCount(url, up)
      yield itemUp
      itemDown = YoukuUtil.get_downCount(url, down)
      yield itemDown
