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
from tracking.items import TrackingItem
from tracking.util.BaseUtil import BaseUtil
from tracking.spiders.spider_base import SpiderBase
reload(sys)
sys.setdefaultencoding('utf-8')

class NeteaseBase(SpiderBase):
  allowed_domains = ['163.com']
  source = 'netease'
  start_urls = []
  channel_name_url = 'http://dy.163.com/wemedia/navinfo'
  base_user_home = 'http://dy.163.com/wemedia/notice/list/1/20.html?wemediaId=%s' # 视频的URL
  base_user_article_home = base_user_home + '&category=' + BaseUtil.Category.ARTICLE # 文章的URL 与视频的URL相同，为了区分，增加'&category=article'

  def __init__(self):
    logging.info("Start to crawl from 163")
    self.start_urls.append(self.channel_name_url)

  def start_requests(self):
    self.load_entity()
    for url in self.start_urls:
      yield scrapy.Request(url, callback=self.parse_channel)

  def parse_channel(self, response):
    channelJson = json.loads(response.body_as_unicode())
    if 'data' in channelJson.keys() and 'tname' in channelJson['data'].keys() and 'wemediaId' in channelJson['data'].keys():
      uid = channelJson['data']['wemediaId']
      if uid != '':
        requests = self.loadRequests(uid)
        for request in requests:
          yield request

  def loadRequests(self, uid):
    raise NotImplementedError()
