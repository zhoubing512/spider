# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import datetime
import scrapy
from scrapy import Selector
from urlparse import urljoin
from scrapy.http import Request
from scrapy.spiders import Spider
from meipai_base import MeipaiBase
from tracking.items import TopicItem, PlaycountItem, RepostItem, CommentsCountItem,  ChannelItem, UpCountItem
from tracking.util.BaseUtil import BaseUtil

GENERAL_CODE = "utf-8"


class MeipaiIndicators(MeipaiBase):
  name = "meipai_indicators_task"

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },
    # 'DOWNLOAD_DELAY': 0.5,
  }

  def loadRequest(self, url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_url))
    requests.append(scrapy.Request(url, callback=self.parse_fans, dont_filter=True))
    return requests

  def loadItems(self, url, topic, playcount, release, repost, commentcount, upcount):
    items = []
    channel = self.target_channel
    itemTopic = BaseUtil.get_topic(url, topic, channel, playcount,release)
    items.append(itemTopic)
    itemPlaycount = BaseUtil.get_playcount(url, channel, playcount, release)
    items.append(itemPlaycount)
    itemRepost = BaseUtil.get_repost(url, repost)
    items.append(itemRepost)
    itemComment = BaseUtil().get_commentscount(url, channel, commentcount)
    items.append(itemComment)
    itemUpcount = BaseUtil().get_upCount(url,upcount)
    items.append(itemUpcount)
    return items

  def parse_fans(self,response):
    id =  response.url
    channel_part = response.xpath('//*[@id="rightUser"]/h3/a/text()').extract_first()
    channel_str = str(BaseUtil().text_clean(channel_part)).decode('utf-8')
    fans = response.xpath('//*[@id="rightUser"]/div[3]/a[4]/span[1]/text()').extract_first()
    itemChannel = BaseUtil().get_channel(id, self.target_channel, fans)
    yield itemChannel
