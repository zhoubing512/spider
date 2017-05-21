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

class UcBase(SpiderBase):
  allowed_domains = ['uc.cn']
  source = 'uc'
  start_urls = []
  url_filter = "uc.cn"
  base_video_url = 'http://napi.uc.cn/3/classes/article/objects/%s?_app_id=cbd10b7b69994dca92e04fe00c05b8c2'
  video_home_url = 'http://a.mp.uc.cn/video.html?uc_param_str=frdnsnpfvecpntnwprdssskt&wm_id=%s&wm_aid=%s'
  base_scan_url = 'http://api.mp.uc.cn/api/v1/users/messages/wemedias/%s?ut=AAT3bpCm2Knl7PLEW7LleJFyRffHZJKD3Q8abzcDH7CZmA%%3D%%3D&app=ucweb&max_pos=%s&size=50'


  def __init__(self):
    logging.info("Start to crawl from uc")

  def start_requests(self):
    self.start_urls = self.load_entity()
    for channel_url in self.start_urls:
      uid = re.search('mid=(\w+)', channel_url).group(1)
      url = self.base_scan_url % (uid, '0')
      yield scrapy.Request(url, callback=self.parse_channel)

  def parse_channel(self, response):
    uid = re.search('wemedias/(\w+)', response.url).group(1)
    jsonObj = json.loads(response.body_as_unicode())
    if 'data' in jsonObj.keys() and len(jsonObj['data']) > 0:
      lastVideoItem = jsonObj['data'][-1]
      if 'pos_str' in lastVideoItem.keys() and 'metadata' in jsonObj.keys() and 'is_whole' in jsonObj['metadata'].keys() and jsonObj['metadata']['is_whole'] == 0:
        pos = lastVideoItem['pos_str']
        if len(pos) > 0:
          uid = re.search('wemedias/(\w+)', response.url).group(1)
          yield scrapy.Request(self.base_scan_url % (uid, pos), callback=self.parse_channel)

      for videoItem in jsonObj['data']:
        if 'msgs' in videoItem.keys() and len(videoItem['msgs']) > 0:
          for msgItem in videoItem['msgs']:
            if 'object_id' in msgItem:
              vid = msgItem['object_id']
              yield scrapy.Request(self.base_video_url % vid, callback=self.parse_items, meta={'uid': uid})

  def parse_items(self, response):
    jsonObj = json.loads(response.body_as_unicode())
    if 'data' in jsonObj.keys():
      data = jsonObj['data']
      url = ''
      topic = ''
      release = 0
      playcount = 0
      commentCount = 0
      pageViewCount = 0
      repostCount = 0
      if '_id' in data.keys():
        url = self.video_home_url % (response.meta['uid'], data['_id'])
      if 'title' in data.keys():
        topic = data['title']
      if 'publish_at' in data.keys():
        release = BaseUtil.datetime2ts(data['publish_at'])
      if 'video_play_times' in data.keys():
        playcount = int(data['video_play_times'])
      if 'comment_times' in data.keys():
        commentCount = int(data['comment_times'])
      if 'show_times' in data.keys():
        pageViewCount = int(data['show_times'])
      if 'shared_times' in data.keys():
        repostCount = int(data['shared_times'])
      items = self.loadItems(url, topic, release, playcount, commentCount, pageViewCount, repostCount)
      for item in items:
        yield item

  def loadItems(self, url, topic, release, playcount, commentCount, pageViewCount, repostCount):
    raise NotImplementedError()
