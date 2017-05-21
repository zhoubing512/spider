# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
import calendar
from datetime import date, datetime, timedelta
from tracking.util.ToutiaoUtil import ToutiaoUtil
from tracking.items import AnalysisItem

reload(sys)
sys.setdefaultencoding('utf-8')

class ToutiaoWeeklyAnalysis(scrapy.Spider):
  name = 'toutiao_weekly_analysis_task'
  allowed_domains = ['toutiao.com']
  source = 'toutiao'
  start_urls = []
  base_video_url = 'https://mp.toutiao.com/statistic/video_stat/?start_date=%s&end_date=%s&pagenum=%s'
  base_weekly_analysis_url = 'https://mp.toutiao.com/statistic/item_related_stat/%s/'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelines.FilePipeline': 301,
    },
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middleware.ToutiaoTrackingCookieMiddleware": 402,
    },
    'CONCURRENT_REQUESTS_PER_IP': 5
  }

  def __init__(self):
    logging.info("Start to crawl from toutiao")
    today = date.today()
    oneday = timedelta(days = 1)
    sevendays = timedelta(days = 7)
    startDay = today - sevendays
    endDay = today - oneday
    self.start_urls.append(self.base_video_url % (startDay, endDay, '1'))
    logging.info('# # # setting date from %s to %s data' % (startDay, endDay))

  def start_requests(self):
    for url in self.start_urls:
      yield scrapy.Request(url, callback=self.parse_videos)

  def parse_videos(self, response):
    jsonObj = {}
    try:
      jsonObj = json.loads(response.body_as_unicode())
    except:
      logging.error("X X X response body is not JSON, url is %s" % response.url)
    if 'data' in jsonObj.keys() and 'data_list' in jsonObj['data'] and len(jsonObj['data']['data_list'])>0:
      data = jsonObj['data']
      pagenum = int(data['pagenum'])
      total_pagenum = int(data['total_pagenum'])
      end_date = data['end_date']
      start_date = data['start_date']
      logging.info('# # # crawl date from %s to %s data' % (start_date, end_date))
      if pagenum < total_pagenum:
        yield scrapy.Request(self.base_video_url % (start_date, end_date, str(pagenum + 1)), callback=self.parse_videos)

      for dataObj in data['data_list']:
        if 'link' in dataObj.keys():
          link = dataObj['link']
          vid = re.search('toutiao.com/i(\d+)', link)
          if vid is not None:
            yield scrapy.Request(self.base_weekly_analysis_url % vid.group(1), callback=self.parse_weekly_analysis)
          else:
            logging.error("X X X can not get video id, link is %s, url is %s" % (link, response.url))
        else:
          logging.error("X X X can not get link, url is %s" % response.url)

    if 'message' in jsonObj.keys():
      if 'success' != jsonObj['message']:
        logging.error("X X X can not get data, message is %s" % response.url)

  def loadItems(self, url, topic, release, playcount, commentCount, pageView, repostCount, recommendationCount):
    requests = []
    vid = re.search('item/(\d+)', url)
    if vid is not None:
      requests.append()
    return requests

  def parse_weekly_analysis(self, response):
    jsonObj = {}
    try:
      jsonObj = json.loads(response.body_as_unicode())
    except:
      logging.warning("X X X response body is not JSON, url is %s" % response.url)
    if 'data' in jsonObj.keys():
      data = jsonObj['data']
      idUrl = ''
      if 'link' in data.keys():
        idUrl = data['link']
        topic = ''
        if 'title' in data.keys():
          topic = data['title']
        progress = 0
        if 'item_read_or_play_avg_progress_pct' in data.keys():
          progress = float(data['item_read_or_play_avg_progress_pct'])
        bounce = 0
        if 'item_read_or_play_avg_bounce_pct' in data.keys():
          bounce = float(data['item_read_or_play_avg_bounce_pct'])
        playtime = 0
        if 'item_play_avg_time' in data.keys():
          playtime = int(data['item_play_avg_time'])
        item = AnalysisItem()
        item['id'] = idUrl
        item['topic'] = topic
        item['progress'] = progress
        item['bounce'] = bounce
        item['playtime'] = playtime
        yield item
