# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import datetime
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import Spider
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, RankingItem
from tracking.util.BaseUtil import BaseUtil
from yidianzixun_base import YidianzixunBase

GENERAL_CODE = "utf-8"

class YidianzixunTracking(YidianzixunBase):
  name = "yidianzixun_tracking_task"
  source = "yidianzixun"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middlewareCookie.CookieMiddleware": 402,
    },

    'DOWNLOAD_DELAY': 0,
    'CONCURRENT_REQUESTS': 16,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    'CONCURRENT_REQUESTS_PER_IP': 16,
  }


  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  def parse_item(self, url, name, play_count, recommendation, cmc, release, title):
    res = []
    tk = BaseUtil.get_tracking(url=url, channel=name, release=release)
    res.append(tk)
    return res
