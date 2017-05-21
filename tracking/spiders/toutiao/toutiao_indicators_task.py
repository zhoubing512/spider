# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib
import scrapy
import logging
from datetime import date, datetime
from toutiao_base import ToutiaoBase
from tracking.util.ToutiaoUtil import ToutiaoUtil
from tracking.items import TopicItem, PlaycountItem, CommentsCountItem, PageviewItem, RepostItem, RecommendationItem, ChannelItem

reload(sys)
sys.setdefaultencoding('utf-8')

class ToutiaoIndicators(ToutiaoBase):
  name = 'toutiao_indicators_task'

  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'CONCURRENT_REQUESTS_PER_IP': 5
  }

  def loadRequest(self, channel_url, url):
    requests = []
    requests.append(scrapy.Request(url, callback=self.parse_channel))
    return requests

  def loadItems(self, url, topic, release, playcount, commentCount, pageView, repostCount, recommendationCount, category):
    items = []
    channel = self.target_channel
    itemTopic = ToutiaoUtil.get_topic(url, topic, channel, playcount, release, category=category)
    items.append(itemTopic)
    itemPlaycount = ToutiaoUtil.get_playcount(url, channel, playcount, release, category=category)
    items.append(itemPlaycount)
    itemCommentCount = ToutiaoUtil.get_commentscount(url,channel,commentCount, category=category)
    items.append(itemCommentCount)
    itemRepost = ToutiaoUtil.get_repost(url, repostCount, category=category)
    items.append(itemRepost)
    itemPageview = ToutiaoUtil.get_pageview(url, pageView, category=category)
    items.append(itemPageview)
    itemRecommendation = ToutiaoUtil.get_recommendation(url, recommendationCount, category=category)
    items.append(itemRecommendation)
    return items
