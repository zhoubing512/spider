# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import datetime
import urllib
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import Spider
from tracking.items import PageviewItem, CommentsCountItem, TopicDuplicateItem, PlaycountDuplicateItem, ChannelItem, TrackingItem
from tracking.util.WeiboUtil import WeiboUtil
from weibo_base import WeiboBase

GENERAL_CODE = "utf-8"


''' 网页版 '''
''' 查询指定的用户的 阅读数, 播放数, 粉丝数, 评论数 '''


class WeiboIndicators(WeiboBase):
  name = "weibo_indicators_task"
  source = "weibo"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
      'tracking.pipelineJsonDuplicate.JsonDupelicatePipeline': 302,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middleware.WeiboCookiesDemoMiddleware": 402,
    },

    'DOWNLOAD_DELAY': 0.5,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS_PER_IP': 1,
  }

  start_urls = [
  ]

  base_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&is_all=1&id=100505%s&script_uri=/u/%s&feed_type=0&domain_op=100505&page=%s&pagebar=%s&pre_page=%s"
  fans_base_url = "http://weibo.com/p/100505%s/home?profile_ftype=1&is_all=1&sudaref=weibo.com"

  blog_base_url = "http://weibo.com/%s/%s"
  user_base_url = "http://weibo.com/u/%s"
  tag = ""
  page_limit = 200

  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # TODO: Load urls from DB

  def start_requests(self):
    self.start_urls = self.load_entity()
    if self.settings["keyword"] is not None:
      self.keywords = urllib.unquote(self.settings["keyword"])
    for url in self.start_urls:
      # Fans:
      uid = re.findall('/u/(\d+)', url)[0]
      yield Request(self.fans_base_url % uid, callback=self.parse_fans, meta={"uid": uid})
      # blog:
      url_group = self.generate_time_line_group(uid, page=1)
      for url in url_group:
        yield Request(url, callback=self.parse_time_line)

  def parse_fans(self, response):
    print "parse_fans", response.url
    # uid = re.findall('100505(\d+)', response.url)[0]
    uid = response.meta["uid"]
    channel_url = self.user_base_url % uid
    fans = re.findall('fans#place.+?" ><strong class=.+?"W_f\d+.+?">(\d+)', response.body)[0]
    name =self.target_channel
    ch = WeiboUtil.get_channel(url=channel_url, name=name, fans=fans)
    yield ch

  def parse_time_line(self, response):
    print response.url
    uid = re.findall('script_uri=\/u\/(\d+)', response.url)[0]
    user_url = self.user_base_url % uid
    this_page = int(re.findall('&page=(\d+)', response.url)[0])
    print "uid", uid, "link", user_url
    hjson = json.loads(response.body.encode(GENERAL_CODE))
    data_html = scrapy.Selector(text=hjson["data"], type="html")
    tables = data_html.xpath('//div[@action-type="feed_list_item"]')

    for table in tables:
      res = self.parse_weibo_table(table, uid)
      if res is None:
        continue
      (blog_url, topic, play_count, release, user_name, data_read, data_cmc, user_name, ts, img) = res
      tp = TopicDuplicateItem()
      pv = PageviewItem()
      cmc = CommentsCountItem()
      pc = PlaycountDuplicateItem()
      tp["id"] = pv["id"] = cmc["id"] = pc["id"] = blog_url
      tp["ts"] = pv["ts"] = cmc["ts"] = pc["ts"] = ts
      tp["category"] = pv["category"] = cmc["category"] = pc["category"] = "video"
      tp["topic"] = topic
      tp["playcount"] = pc["playcount"] = play_count
      tp["release"] = pc["release"] = release
      tp["channel"] = cmc["channel"] = pc["channel"] = user_name
      pv["view"] = data_read
      cmc["count"] = data_cmc
      tp["key"] = pc["key"] = img
      #yield pv
      yield tp
      yield cmc
      yield pc

    # 翻页
    next_urls = self.parse_next_page(data_html, uid, this_page)
    for next in next_urls:
      yield Request(next, callback=self.parse_time_line)

