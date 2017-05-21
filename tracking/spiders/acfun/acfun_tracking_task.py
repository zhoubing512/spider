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
from acfun_base import AcfunBase

GENERAL_CODE = "utf-8"

class AcfunTracking(AcfunBase):
  name = "acfun_tracking_task"
  source = "acfun"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },

    'DOWNLOAD_DELAY': 0,
    'CONCURRENT_REQUESTS': 16,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    'CONCURRENT_REQUESTS_PER_IP': 16,
  }


  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  def parse_av_list(self, av_id, url, name, topic, view, release):
    res = []
    tk = BaseUtil.get_tracking(url=url, channel=name, release=release)
    res.append(tk)
    return res
