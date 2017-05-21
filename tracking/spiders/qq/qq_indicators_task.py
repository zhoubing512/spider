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
from qq_base import QqBase

GENERAL_CODE = "utf-8"

class QqIndicators(QqBase):
  name = "qq_indicators_task"
  source = "qq"
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

  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  def parse_item(self, url, name, topic, play_count, release):
    res = []
    tp = BaseUtil.get_topic(url=url, topic=topic, channel=name, playcount=play_count, release=release, )
    res.append(tp)
    pc = BaseUtil.get_playcount(url=url, channel=name, playcount=play_count, release=release)
    res.append(pc)
    cid = re.findall('\/(\w+)\.htm', url)[0]
    res.append(Request(url=self.base_cmt_id_url % (cid, cid), callback=self.parse_cid))
    return res

  def parse_cid(self, response):
    hjson = re.findall('(\{.+\})', response.body)[0]
    hjson = json.loads(hjson, encoding=GENERAL_CODE)
    comment_id = hjson["comment_id"]
    srcid = hjson["srcid"]
    yield Request(url=self.base_start_cmt_url % (comment_id, srcid), callback=self.parse_cmc)

  def parse_cmc(self, response):
    oriId = re.search('orilink=(\w*)', response.url).group(1)
    oriUrl = self.base_sub_url % oriId
    hjson = json.loads(response.body, encoding=GENERAL_CODE)
    commentnum = int(hjson["data"]["targetinfo"]["commentnum"])
    cmc = BaseUtil.get_commentscount(url=oriUrl, channel=self.target_channel, count=commentnum)
    yield cmc
