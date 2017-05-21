
import re
import sys
import json
import time
import urllib
import scrapy
import logging
from datetime import date, datetime
from tracking.util.BaseUtil import BaseUtil
from tracking.spiders.spider_base import SpiderBase
reload(sys)
sys.setdefaultencoding('utf-8')

class SohuBase(SpiderBase):
  allowed_domains = ['sohu.com']
  source = 'sohu'
  start_urls = []
  url_filter = "sohu.com"
  base_scan_url = 'http://my.tv.sohu.com/user/wm/ta/v.do?uid=%s&pg=%s&size=50&sortType=2' #310035774:haohaochi

  def __init__(self):
    logging.info("Start to crawl from sohu")

  def start_requests(self):
    self.start_urls = self.load_entity()
    for channel_url in self.start_urls:
      logging.info('# # # Sohu channel url: %s' % channel_url)
      uidObj = re.search('user/(\d+)', channel_url)
      if uidObj is not None:
        requests = self.loadRequests(uidObj.group(1), channel_url)
        for request in requests:
          yield request

  def parse_channel(self, response):
    jsonObj = json.loads(response.body_as_unicode())
    if 'data' in jsonObj.keys():
      uid = response.meta['uid']
      jsonData = jsonObj['data']
      if 'haveMore' in jsonData.keys() and jsonData['haveMore'] is True:
        pageNum = 0
        if 'pg' in jsonData.keys():
          nextPageNum = int(jsonData['pg']) + 1
        else:
          nextPageNum = int(re.search('&pg=(\d+)&', response.url).group(1)) + 1
        if nextPageNum > 1:
          nextPageUrl = self.base_scan_url % (uid, nextPageNum)
          yield scrapy.Request(nextPageUrl, callback=self.parse_channel, meta={'uid': uid})
      if 'list' in jsonObj['data'].keys() and len(jsonObj['data']['list'])>0:
        videos = jsonObj['data']['list']
        if videos is not None and len(videos)>0:
          for video in videos:
            topic = ''
            release = 0
            url = ''
            if 'title' in video.keys():
              topic = video['title']
            if 'uploadTime' in video.keys():
              release = int(video['uploadTime'])/1000
            if 'url' in video.keys():
              url = video['url']
            if 'id' in video.keys():
              vid = video['id']
              if vid != '':
                items = self.loadItems(vid, url, topic, release)
                for item in items:
                  yield item

  def loadRequests(self, uid, channel_url):
    raise NotImplementedError()

  def loadItems(self, vid, url, topic, release):
    raise NotImplementedError()
