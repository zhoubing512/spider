# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from urlparse import urljoin
from uc_base import UcBase
from datetime import date, datetime
from tracking.util.BaseUtil import BaseUtil
from tracking.items import TopicItem, PlaycountItem, ChannelItem

reload(sys)
sys.setdefaultencoding('utf-8')

class UcIndicators(UcBase):
  name = 'uc_indicators_task'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    "DOWNLOADER_MIDDLEWARES": {
      "tracking.middleware.UserAgentMiddleware": 401,
    },
    'DOWNLOAD_DELAY':0.2,
  }

  def loadItems(self, url, topic, release, playcount, commentCount, pageViewCount, repostCount):
    items = []
    channel = self.target_channel
    itemTopic = BaseUtil.get_topic(url, topic, channel, playcount, release)
    items.append(itemTopic)
    itemPlaycount = BaseUtil.get_playcount(url, channel, playcount, release)
    items.append(itemPlaycount)
    itemCommentCount = BaseUtil.get_commentscount(url,channel,commentCount)
    items.append(itemCommentCount)
    itemRepost = BaseUtil.get_repost(url, repostCount)
    items.append(itemRepost)
    itemPageview = BaseUtil.get_pageview(url, pageViewCount)
    items.append(itemPageview)
    return items
