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

class IqiyiBase(SpiderBase):
  allowed_domains = ['iqiyi.com']
  source = 'iqiyi'
  start_urls = []
  url_filter = "iqiyi.com"
  base_video_url = 'http://mixer.video.iqiyi.com/jp/mixin/videos/%s'
  base_scan_url = 'http://www.iqiyi.com/u/%s/v?page=%s&video_type=1'

  def __init__(self):
    logging.info("Start to crawl from iqiyi")

  def start_requests(self):
    self.start_urls = self.load_entity()
    for channel_url in self.start_urls:
      logging.info('# # # Iqiyi channel url: %s' % channel_url)
      uidObj = re.search('/u/(\d+)', channel_url)
      if uidObj is not None:
        url = self.base_scan_url % (uidObj.group(1),'1')
        logging.info('# # # Iqiyi start url: %s' % url)
        requests = self.loadRequest(channel_url, url)
        for request in requests:
          yield request

  def parse_vid(self, response):
    uid = re.search('/u/(\d+)', response.url).group(1)
    pageObj = response.xpath('//a[@class="a1"]/@href').extract()
    if pageObj is not None and len(pageObj)>0:
      pageNum = re.search('page=(\d+)', pageObj[-1])
      if pageNum is not None:
        nextPageUrl = self.base_scan_url % (uid, pageNum.group(1))
        yield scrapy.Request(nextPageUrl, callback=self.parse_vid)
    liObjs = response.xpath('//div[@class="wrap-customAuto-ht "]/ul/li')
    for liObj in liObjs:
      tvid = liObj.xpath('./@tvid').extract_first()
      if tvid is not None:
        yield scrapy.Request(self.base_video_url % tvid, callback=self.parse_channel)

  def parse_channel(self, response):
    body = response.body_as_unicode()
    jsonStr = body[body.find('tvInfoJs=')+9:]
    jsonObj = json.loads(jsonStr)
    topic = ''
    release = 0
    url = ''
    playcount = 0
    upCount = 0
    downCount = 0
    commentCount = 0
    if 'url' in jsonObj.keys():
      url = jsonObj['url']
    if 'name' in jsonObj.keys():
      topic = jsonObj['name']
    if 'playCount' in jsonObj.keys():
      playcount = int(jsonObj['playCount'])
    if 'upCount' in jsonObj.keys():
      upCount = int(jsonObj['upCount'])
    if 'downCount' in jsonObj.keys():
      downCount = int(jsonObj['downCount'])
    if 'issueTime' in jsonObj.keys():
      release = int(jsonObj['issueTime'])/1000
    if 'commentCount' in jsonObj.keys():
      commentCount = int(jsonObj['commentCount'])/1000
    items = self.loadItems(url, topic, release, playcount, commentCount, upCount, downCount)
    for item in items:
      yield item

  def loadRequest(self, url, channel_url):
    raise NotImplementedError()

  def loadItems(self, url, topic, release, playcount, commentCount, upCount, downCount):
    raise NotImplementedError()
