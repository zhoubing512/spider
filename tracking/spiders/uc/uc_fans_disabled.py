# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from urlparse import urljoin
from datetime import date, datetime,timedelta
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TopicItem, PlaycountItem, ChannelItem

reload(sys)
sys.setdefaultencoding('utf-8')

class UcFans(scrapy.Spider):
  name = 'uc_fans_task'
  allowed_domains = ['uc.cn.com']
  source = 'uc'
  start_urls = []

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middleware.UcFansCookieMiddleware": 402,
    },
    'DOWNLOAD_DELAY':0.2,
  }
  base_user_url = 'http://mp.uc.cn/dashboard/index'
  base_fans_url = 'http://mp.uc.cn/api/ws/stat/users/details?size=10&begin_date=%s&end_date=%s&page=1&_=1493279020240'

  def __init__(self):
    logging.info("Start to crawl from uc")
    yesterday = (datetime.now()+timedelta(days=-1)).strftime('%Y%m%d')
    self.start_urls.append(self.base_fans_url % (yesterday, yesterday))

  def start_requests(self):
    for url in self.start_urls:
      yield scrapy.Request(url, callback=self.parse_fans)

  def parse_fans(self, response):
    jsonObj = json.loads(response.body_as_unicode())
    if 'data' in jsonObj.keys() and len(jsonObj['data'])>0:
      fanObj = jsonObj['data'][0]
      fansCount = 0
      if 'follow_times_total' in fanObj.keys():
        fansCount = int(fanObj['follow_times_total'])
      item = BaseUtil.get_channel(self.base_user_url, '好好吃', fansCount)
      yield item
    if 'error' in jsonObj.keys() and 'message' in jsonObj['error'].keys():
      logging.error("X X　X Reuqest error: %s" % jsonObj['error']['message'])
