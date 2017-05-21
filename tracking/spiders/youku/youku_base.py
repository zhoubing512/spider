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
from tracking.util.YoukuUtil import YoukuUtil
from tracking.spiders.spider_base import SpiderBase
reload(sys)
sys.setdefaultencoding('utf-8')

class YoukuBase(SpiderBase):
  allowed_domains = ['youku.com']
  source = 'youku'
  start_urls = []
  url_filter = "youku.com"
  base_user_url = 'http://i.youku.com/i/%s/videos?order=1&page=%s'
  base_video_url = 'http://v.youku.com/v_show/id_%s.html'

  def __init__(self):
    logging.info("Start to crawl from youku")

  def start_requests(self):
    self.start_urls = self.load_entity()
    for channel_url in self.start_urls:
      logging.info('# # # Youku channel url: %s' % channel_url)
      uidObj = re.search('youku.com/i/(\w+=*)', channel_url)
      if uidObj is not None:
        url = self.base_user_url % (uidObj.group(1), '1')
        logging.info('# # # Youku start url: %s' % url)
        requests = self.loadRequest(url)
        for request in requests:
          yield request

  def parse_channel(self, response):
    nextPageObj = response.xpath('//li[@class="next"]/a/@href').extract_first()
    if nextPageObj is not None:
      nextPageUrl = urljoin(self.base_user_url, nextPageObj)
      if nextPageUrl is not None:
        yield scrapy.Request(nextPageUrl, callback=self.parse_channel)

    itemObjs = response.xpath('//div[@class="v-meta"]')
    for itemObj in itemObjs:
      release = ''
      aTag = itemObj.xpath('./div[@class="v-meta-title"]/a')
      url = aTag.xpath('./@href').extract_first()
      vidObj = re.search('v_show/id_(\w+=*).html', url)
      if vidObj is not None:
        url = self.base_video_url % vidObj.group(1)
      elif url.startswith("//"):
        url = urljoin('http:', url)
      topic = aTag.xpath('./@title').extract_first()
      spanTag = itemObj.xpath('./div[@class="v-meta-entry"]')
      releaseObj = spanTag.xpath('./span[@class="v-publishtime"]/text()').extract_first()
      if releaseObj is not None:
        releaseObj = YoukuUtil.format_youku_time(releaseObj)
        if releaseObj is not None:
          release = int(releaseObj)
      items = self.loadItems(url, topic, release)
      for item in items:
        yield item

  def loadRequest(self, url):
    raise NotImplementedError()

  def loadItems(self, url, topic, release):
    raise NotImplementedError()
