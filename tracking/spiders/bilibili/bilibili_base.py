# -*- coding: utf-8 -*-
#
import re
import sys
import json
import time
import urllib
import scrapy
import logging
from scrapy import Request
from datetime import date, datetime
from tracking.spiders.spider_base import SpiderBase
from tracking.util.BaseUtil import BaseUtil

reload(sys)
sys.setdefaultencoding('utf-8')

class BilibiliBase(SpiderBase):
  allowed_domains = ['bilibili.com']
  source = 'bilibili'
  start_urls = []
  url_filter = "bilibili.com"
  base_user_url = 'http://space.bilibili.com/%s/#!/'
  meta_url = 'http://space.bilibili.com/ajax/friend/GetFansList?mid=%s&page=1&_=1492997597320'
  channel_home_url = 'http://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s&ts=1492992555645&page=%s&pagesize=%s'
  page_size = 20
  custom_settings = {
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
    }
  }

  def __init__(self):
    logging.info("Start to crawl from bilibili")

  def start_requests(self):
    self.start_urls = self.load_entity()
    for channel_url in self.start_urls:
      logging.info('# # # Bilibili channel url: %s' % channel_url)
      uidObj = re.search('bilibili.com/(\d+)', channel_url)
      if uidObj is not None:
        uid = uidObj.group(1)
        url = self.generate_list_url(uid, 1)
        logging.info('# # # Bilibili start url: %s' % url)
        requests = self.loadRequest(uid, url)
        for request in requests:
          yield request

  def parse_channel(self, response):
    logging.info('# # # Bilibili channel url: %s' % response.url)
    jsonObj = json.loads(response.body_as_unicode())
    if 'data' in jsonObj.keys() and 'vlist' in jsonObj['data'].keys():
      videos = jsonObj['data']['vlist']
      for video in videos:
        url = ''
        if 'aid' in video.keys():
          url = "http://www.bilibili.com/video/av" + str(video['aid']) + "/"
        release = 0
        if 'created' in video.keys():
          release = int(video['created'])
        topic = ''
        if 'title' in video.keys():
          topic = video['title']
        playcount = 0
        if 'play' in video.keys():
          playcount = int(video['play'])
        barrageCount = 0
        if 'comment' in video.keys():
          barrageCount = int(video['comment'])
        commentCount = 0
        if 'review' in video.keys():
          commentCount = int(video['review'])
        if url != '':
          commentCount += barrageCount
          items = self.loadItems(url, topic, release, playcount, commentCount)
          for item in items:
            yield item
      total_count = int(jsonObj["data"]["count"])
      this_page = int(re.findall('page=(\d+)', response.url)[0])
      if (this_page * self.page_size) < total_count:
        uid = int(re.findall('mid=(\d+)', response.url)[0])
        next_url = self.generate_list_url(uid, this_page + 1)
        yield Request(url=next_url, callback=self.parse_channel, dont_filter=True)

  def loadRequest(self, uid, url):
    raise NotImplementedError()

  def loadItems(self, url, topic, release, playcount, commentCount):
    raise NotImplementedError()

  def generate_list_url(self, uid, page):
    return self.channel_home_url % (uid, page, self.page_size)
