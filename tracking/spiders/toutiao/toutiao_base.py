
import re
import sys
import json
import time
import urllib
import scrapy
import logging
from datetime import date, datetime
from tracking.util.ToutiaoUtil import ToutiaoUtil
from tracking.spiders.spider_base import SpiderBase

class ToutiaoBase(SpiderBase):
  allowed_domains = ['toutiao.com', 'snssdk.com']
  source = 'toutiao'
  start_urls = []
  url_filter = "toutiao.com"
  base_media_scan_url = 'http://www.toutiao.com/pgc/ma/?media_id=%s&page_type=1&max_behot_time=%s&count=20&version=2&platform=app&as=%s' #page_type=1  videos & article; page_type=0  videos

  custom_settings = {
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
    },
    'DOWNLOAD_DELAY':0.2,
    'DOWNLOAD_DELAY_WHEN_JSON_CRASH':2
  }

  reload(sys)
  sys.setdefaultencoding('utf-8')

  def __init__(self):
    logging.info("Start to crawl from toutiao")
    self.retryDict = {}
    self.retryTimes = 0

  def start_requests(self):
    self.start_urls = self.load_entity()
    asstr = ToutiaoUtil.generateAS()
    for channel_url in self.start_urls:
      logging.info('# # # Toutiao channel url: %s' % channel_url)
      mediaIdObj = re.search('mid=(\d+)', channel_url)
      if mediaIdObj is not None:
        url = self.base_media_scan_url % (mediaIdObj.group(1),'0', asstr)
        logging.info('# # # Toutiao start url: %s' % url)
        requests = self.loadRequest(channel_url, url)
        for request in requests:
          yield request

  def parse_channel(self, response):
    jsonObj = json.loads(response.body_as_unicode())
    videos = jsonObj['data']
    for video in videos:
      # id
      link = ''
      ts = ToutiaoUtil.date_time_now()
      display = video
      if(display.has_key('display')):
        display = display['display']
      if 'source_url' in display.keys():
        link = display['source_url']
      elif 'display_url' in display.keys():
        link = display['display_url']
      elif 'url' in display.keys():
        link = display['url']
      elif 'article_url' in display.keys():
        link = display['article_url']
      else:
        return
      if '?' in link:
        link = link[:link.find('?')]
      # # channel
      # channel = ''
      # if 'source' in display.keys():
      #   channel = display['source']
      # release
      release = 0
      if 'publish_time' in display.keys():
        release = int(display['publish_time'])
      # topic
      topic = ''
      if 'title' in display.keys():
        topic = display['title']
      # playcount
      playcount = 0
      list_play_count = 0
      detail_play_count = 0
      if 'list_play_effective_count' in display.keys():
        list_play_count = int(display['list_play_effective_count'])
      if 'detail_play_effective_count' in display.keys():
        detail_play_count = int(display['detail_play_effective_count'])
      pageView = 0
      if 'total_read_count' in display.keys():
        pageView = int(display['total_read_count'])
      category = ToutiaoUtil.Category.VIDEO
      if display['has_video'] is True:
        playcount = list_play_count + detail_play_count
      else:
        category = ToutiaoUtil.Category.ARTICLE
        playcount = pageView
      # comment_count
      cmtCount = 0
      if 'comment_count' in display.keys():
        cmtCount = int(display['comment_count'])
      # page view
      # repost count
      repostCount = 0
      if 'share_count' in display.keys():
        repostCount = int(display['share_count'])
      # recommendation Count
      recommendationCount = 0
      if 'impression_count' in display.keys():
        recommendationCount = int(display['impression_count'])
      if link is not None:
        items = self.loadItems(link, topic, release, playcount, cmtCount, pageView, repostCount, recommendationCount, category)
        for item in items:
          yield item
    #
    currentUrl = response.url
    nextUrl = ''
    sleepTime = 0
    isRetry = False
    asstr = ToutiaoUtil.generateAS()
    if 'has_more' in jsonObj.keys() and 'next' in jsonObj.keys():
      nextObj = jsonObj['next']['max_behot_time']
      mid = re.search('media_id=(\d+)', currentUrl).group(1)
      if jsonObj['has_more'] == 1:
        nextUrl = self.base_media_scan_url % (mid, nextObj, asstr)
      elif jsonObj['has_more'] is False:
        behot = re.search('max_behot_time=(\d+)', currentUrl).group(1)
        key = mid + '-' + behot
        if self.retryDict.has_key(key):
          self.retryDict[key] = int(self.retryDict[key]) + 1
        else:
          self.retryDict[key] = 1
        if int(self.retryDict[key])<=self.retryTimes:
          logging.info('Retry times >>>>>>>>>>>>>>>>>>>>>>>>%s ' % int(self.retryDict[key]))
          sleepTime = int(self.settings['DOWNLOAD_DELAY_WHEN_JSON_CRASH']) * int(self.retryDict[key])
          nextUrl = self.base_media_scan_url % (mid, behot, asstr)
          isRetry=True
        else:
          logging.warning('Cannot get json in %d times !!!!!!!!!!!!!!!!!!!!!!!! %s' % (self.retryTimes,currentUrl))
    if nextUrl != '':
      time.sleep(sleepTime)
      yield scrapy.Request(nextUrl, callback=self.parse_channel, dont_filter=isRetry)

  def loadRequest(self, channel_url, url):
    raise NotImplementedError()

  def loadItems(self, url, topic, release, playcount, cmtCount, pageView, repostCount, recommendationCount, category):
    raise NotImplementedError()
