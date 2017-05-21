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
from tracking.util.TrackingUtil import TrackingUtil
from tracking.spiders.spider_base import SpiderBase
from autohome_base import AutohomeBase

GENERAL_CODE = "utf-8"

class AutohomeIndicators(AutohomeBase):
  name = "autohome_indicators_task"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },

    'DOWNLOAD_DELAY': 0.1,
    'CONCURRENT_REQUESTS': 16,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    'CONCURRENT_REQUESTS_PER_IP': 16,
  }


  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  channel_base = "http://youchuang.autohome.com.cn/Authors/%s"

  def parse_user(self, response):
    print response.url
    core_fan = response.xpath('.//div[@class="r-core-fan"]/span[@class="core-mr"]/font/i')\
      .xpath('string(.)').extract_first()
    fans = int(core_fan)
    uid = re.findall("Authors/(\d+)", response.url)[0]
    url = self.generate_channel_url(uid)
    ch = BaseUtil.get_channel(url=url, name=self.target_channel, fans=fans)
    yield ch

  def parse_item(self, url, name, release, play_count, cmc, title, category):
    res = []
    tp = BaseUtil.get_topic(url=url, topic=title, channel=name, release=release, playcount=play_count, category=category)
    res.append(tp)
    pc = BaseUtil.get_playcount(url=url, channel=name, playcount=play_count, release=release, category=category)
    res.append(pc)
    cmc = BaseUtil.get_commentscount(url=url, channel=name, count=cmc, category=category)
    res.append(cmc)
    return res

  def generate_channel_url(self, uid):
    return self.channel_base % uid

