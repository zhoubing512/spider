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

class AcfunIndicators(AcfunBase):
  name = "acfun_indicators_task"
  source = "acfun"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
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

  def parse_av_list(self, av_id, url, name, topic, view, release):
    res = []
    tp = BaseUtil.get_topic(url=url, topic=topic, channel=name, release=release, playcount=view)
    res.append(tp)
    pc = BaseUtil.get_playcount(url=url, channel=name, playcount=view, release=release)
    res.append(pc)
    req = self.generate_cmc_url(av_id, 1)
    res.append(req)
    return res

  def parse_comment(self, response):
    hjson = json.loads(response.body, encoding=GENERAL_CODE)
    av_d = re.findall('contentId=(\d+)', response.url)[0]
    av_url = self.av_url_base_s % av_d
    totalCount = int(hjson["data"]["totalCount"])
    comment = BaseUtil.get_commentscount(url=av_url, channel=self.target_channel, count=totalCount)
    yield comment

    # totalPage = int(hjson["data"]["totalPage"])
    # page = int(hjson["data"]["page"])
    # for cmc in hjson["data"]["commentContentArr"]:
    #   isDelete = bool(cmc["isDelete"])
    #   if isDelete:
    #     continue
    #   cid = cmc["cid"]
    #   content = cmc["content"]
    #   postDate = cmc["postDate"]
    #   userName = cmc["userName"]
    #   userID = cmc["userID"]
    #   user_url = self.user_url_base % userID
    # if page < totalPage:
    #   next_page = self.generate_cmc_url(av_d, page + 1)
    #   yield Request(url=next_page, callback=self.parse_comment)

  def generate_cmc_url(self, avid, page):
    av_d = int(re.findall('(\d+)', avid)[0])
    url = self.cmc_base % (av_d, page)
    return Request(url=url, callback=self.parse_comment)
