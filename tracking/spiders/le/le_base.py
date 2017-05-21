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

class LeBase(SpiderBase):
  allowed_domains = ['le.com']
  source = 'le'
  start_urls = []
  url_filter = "le.com"
  base_video_url = 'http://www.le.com/ptv/vplay/%s.html'
  base_scan_url = 'http://chuang.le.com/u/%s/queryvideolist?orderType=0&currentPage=%s&pageSize=48'

  def __init__(self):
    logging.info("Start to crawl from youku")

  def start_requests(self):
    self.start_urls = self.load_entity()
    for channel_url in self.start_urls:
      logging.info('# # # Le channel url: %s' % channel_url)
      uidObj = re.search('le.com/u/(\d+)', channel_url)
      if uidObj is not None:
        url = self.base_scan_url % (uidObj.group(1), '1')
        yield scrapy.Request(url, callback=self.parse_channel)

  def parse_channel(self, response):
    jsonStr = re.search('null\((.*)\)', response.body_as_unicode())
    jsonObj = json.loads(jsonStr.group(1))
    if 'data' in jsonObj.keys() and 'list' in jsonObj['data'].keys():
      jsonData = jsonObj['data']
      videos = jsonObj['data']['list']
      uid = re.search('le.com/u/(\d+)', response.url).group(1)
      currentPage = 0
      totalPage = 0
      if 'currentPage' in jsonData.keys():
        currentPage = int(jsonData['currentPage'])
      if 'totalPage' in jsonData.keys():
        totalPage = int(jsonData['totalPage'])
      nextPageNum = currentPage + 1
      if nextPageNum <= totalPage:
        nextPageUrl = self.base_scan_url % (uid, str(nextPageNum))
        yield scrapy.Request(nextPageUrl, callback=self.parse_channel)

      for video in videos:
        topic = ''
        playcount = 0
        vid = ''
        if 'title' in video.keys():
          topic = video['title']
        if 'hits' in video.keys():
          playcount = int(video['hits'])
        if 'vid' in video.keys():
          vid = video['vid']
        if len(str(vid))>0:
          url = self.base_video_url % vid
          yield scrapy.Request(url, callback=self.parse_release, meta={'topic':topic,'playcount':playcount})

  def parse_release(self, response):
    if 'error' in response.url:
      return
    vid = ''
    url = response.url
    topic = response.meta['topic']
    playcount = response.meta['playcount']
    release = 0
    releaseObj = response.xpath('//b[@class="b_02"]/text()').extract_first()
    if releaseObj is not None:
      release = BaseUtil.datetime2ts(releaseObj)
    vidObj = re.search('vplay/(\d+).html', response.url)
    if vidObj is not None:
      vid = vidObj.group(1)
    items = self.loadItems(vid, url, topic, release, playcount)
    for item in items:
      yield item

  def loadItems(self, vid, url, topic, release, playcount):
    raise NotImplementedError()
