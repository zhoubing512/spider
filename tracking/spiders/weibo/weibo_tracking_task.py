# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import datetime
import scrapy
import urllib
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import Spider
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, ChannelItem, TrackingItem
from tracking.util.WeiboUtil import WeiboUtil
from weibo_base import WeiboBase

GENERAL_CODE = "utf-8"


class WeiboTracking(WeiboBase):
  name = "weibo_tracking_task"
  source = "weibo"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineTagMonitor.MonitorPipeline': 302,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middleware.WeiboCookiesDemoMiddleware": 402,
    },

    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS_PER_IP': 1,
  }

  start_urls = [
  ]

  base_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&is_all=1&id=100505%s&script_uri=/u/%s&feed_type=0&domain_op=100505&page=%s&pagebar=%s&pre_page=%s"
  fans_base_url = "http://weibo.com/p/100505%s/follow?relate=fans"

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
      uid = re.findall('/u/(\d+)', url)[0]
      url_group = self.generate_time_line_group(uid, page=1)
      for url in url_group:
        yield Request(url, callback=self.parse_time_line)

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
      tk = TrackingItem()
      tk["id"] = blog_url
      tk["channel"] = user_name
      tk["release"] = release
      yield tk

    # 翻页
    next_urls = self.parse_next_page(data_html, uid, this_page)
    for next in next_urls:
      yield Request(next, callback=self.parse_time_line)

