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

class YidianzixunIndicators(YidianzixunBase):
  name = "yidianzixun_indicators_task"
  source = "yidianzixun"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
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

  cmc_base = "http://www.acfun.cn/comment_list_json.aspx?isNeedAllCount=true&contentId=%d&currentPage=%d"

  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  def parse_item(self, url, name, play_count, recommendation, cmc, release, title):
    res = []
    tp = BaseUtil.get_topic(url=url, topic=title, channel=name, release=release, playcount=play_count)
    res.append(tp)

    pc = BaseUtil.get_playcount(url=url, channel=name, playcount=play_count, release=release)
    res.append(pc)

    rec = BaseUtil.get_recommendation(url=url, count=recommendation)
    res.append(rec)

    rec = BaseUtil.get_commentscount(url=url, channel=name, count=cmc)
    res.append(rec)
    return res

  def parse_user(self, response):
    hjson = json.loads(response.body, encoding=GENERAL_CODE)
    fans = int(hjson["result"]["orders"])
    url = self.start_urls[0]
    ch = BaseUtil.get_channel(url=url, name=self.target_channel, fans=fans)
    yield ch

