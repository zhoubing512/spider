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
from netease_base import NeteaseBase
from tracking.items import TrackingItem
from tracking.util.BaseUtil import BaseUtil
reload(sys)
sys.setdefaultencoding('utf-8')

class NeteaseTracking(NeteaseBase):
  name = 'netease_tracking_task'
  channel_video_url = 'http://dy.163.com/wemedia/video/mylist/%s/%s-20.html'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
        'tracking.pipelineMonitor.MonitorPipeline': 302,
    },
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
      # "tracking.middleware.NeteaseTrackingCookieMiddleware": 402,
      "tracking.middlewareCookie.CookieMiddleware": 402,
    },
    'DOWNLOAD_DELAY':0.2
  }

  def loadRequests(self, uid):
    requests = []
    requests.append(scrapy.Request(self.channel_video_url % (uid, '1'), callback=self.parse_tracking, meta={'uid': uid}))
    return requests

  def parse_tracking(self, response):
    uid = response.meta['uid']
    pageNumObj = re.search('%s/(\d+)-20.html' % uid, response.url)
    if pageNumObj is not None:
      nextPageNum = int(pageNumObj.group(1)) + 1
      nextPageUrl = self.channel_video_url % (uid, str(nextPageNum))
      nextpageStr = '%s/%s-20.html' % (uid , str(nextPageNum))
      pageElements = response.xpath('//a[@class="next"]/@href').extract()
      for pe in pageElements:
        if nextpageStr in pe:
          yield scrapy.Request(nextPageUrl, callback=self.parse_tracking, meta={'uid': uid})
      trs = response.xpath('//tbody/tr')
      for tr in trs:
        url = tr.xpath('.//td/a[@class="article-title"]/@href').extract_first()
        release = tr.xpath('./td[2]/text()').extract_first()
        release = BaseUtil.datetime2ts(release)
        item = BaseUtil.get_tracking(url,self.target_channel,release)
        yield item
