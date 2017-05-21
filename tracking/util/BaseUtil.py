# -*- coding: utf-8 -*-

import re
import datetime
import json
import time
import urllib2
from tracking.items import *


class BaseUtil(object):
  def enum(**enums):
    return type('Enum', (), enums)

  Category = enum(VIDEO='video', ARTICLE='article')

  def __init__(self):
    pass

  @staticmethod
  def text_clean(text):
    t = text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace(',', ' ').strip()
    t = re.sub('\s+', ' ', t)
    return t

  @staticmethod
  def json_clean(text):
    t = text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').strip()
    return t

  @staticmethod
  def date_time_now():
    return int(datetime.datetime.now().strftime('%s'))

  # 日期转时间戳
  @staticmethod
  def date2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

  # 日期时间转时间戳
  @staticmethod
  def datetime2ts(datetime):
    return int(time.mktime(time.strptime(datetime, '%Y-%m-%d %H:%M:%S')))

  @staticmethod
  def convert_playcount(raw):
    number = 0
    base_number = 1
    if raw is not None:
      source = raw.replace(',', '')
      numstr = re.search('(\d+[.]*\d*)', source)
      if numstr is not None:
        number = float(numstr.group(1))
        if u'万' in source:
          base_number = 10000
        elif u'亿' in source:
          base_number = 100000000
    return int(base_number*number)

  @staticmethod
  def cookie2dict(cookie):
    lst = re.split(';{1} *', cookie)
    result = dict()
    for i in lst:
      row = re.split('=', i, 1)
      if len(row) > 1:
        result[row[0]] = row[1]
    return result

  @staticmethod
  def get_topic(url, topic, channel, playcount, release, ts="", category=Category.VIDEO):
    item = TopicItem()
    item["id"] = url
    item["topic"] = topic
    item["channel"] = channel
    item["release"] = int(release)
    item["playcount"] = int(playcount)
    item["ts"] = ts if isinstance(ts, int) else BaseUtil.date_time_now()
    item['category'] = category
    return item

  @staticmethod
  def get_playcount(url, channel, playcount, release, ts="", category=Category.VIDEO):
    item = PlaycountItem()
    item["id"] = url
    item["channel"] = channel
    item["playcount"] = int(playcount)
    item["release"] = int(release)
    item["ts"] = ts if isinstance(ts, int) else BaseUtil.date_time_now()
    item['category'] = category
    return item

  @staticmethod
  def get_commentscount(url, channel, count, ts="", category=Category.VIDEO):
    item = CommentsCountItem()
    item["id"] = url
    item["channel"] = channel
    item["count"] = int(count)
    item["ts"] = ts if isinstance(ts, int) else BaseUtil.date_time_now()
    item['category'] = category
    return item

  @staticmethod
  def get_tracking(url, channel, release):
    item = TrackingItem()
    item["id"] = url
    item["channel"] = channel
    item["release"] = int(release)
    return item

  @staticmethod
  def get_channel(url, name, fans, ts=""):
    item = ChannelItem()
    item["id"] = url
    item["name"] = name
    item["fans"] = int(fans)
    item["ts"] = ts if isinstance(ts, int) else BaseUtil.date_time_now()
    return item

  @staticmethod
  def get_upCount(url, upCount, ts="", category=Category.VIDEO):
    item = UpCountItem()
    item["id"] = url
    item["count"] = int(upCount)
    item["ts"] = ts if isinstance(ts, int) else BaseUtil.date_time_now()
    item['category'] = category
    return item

  @staticmethod
  def get_downCount(url, downCount, ts="", category=Category.VIDEO):
    item = DownCountItem()
    item["id"] = url
    item["count"] = int(downCount)
    item["ts"] = ts if isinstance(ts, int) else BaseUtil.date_time_now()
    item['category'] = category
    return item

  @staticmethod
  def get_recommendation(url, count, ts="", category=Category.VIDEO):
    item = RecommendationItem()
    item["id"] = url
    item["recommendationCount"] = int(count)
    item["ts"] = ts if isinstance(ts, int) else BaseUtil.date_time_now()
    item['category'] = category
    return item

  @staticmethod
  def get_repost(url, repostCount, ts="", category=Category.VIDEO):
    item = RepostItem()
    item["id"] = url
    item["repostCount"] = int(repostCount)
    item["ts"] = ts if isinstance(ts, int) else BaseUtil.date_time_now()
    item['category'] = category
    return item

  @staticmethod
  def get_pageview(url, view, ts="", category=Category.VIDEO):
    item = PageviewItem()
    item["id"] = url
    item["view"] = int(view)
    item["ts"] = ts if isinstance(ts, int) else BaseUtil.date_time_now()
    item['category'] = category
    return item

  @staticmethod
  def parse_response(url):
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    html = res.read()
    hjson = json.loads(html)
    return hjson
