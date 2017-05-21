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
from tracking.util.QqUtil import QqUtil
from tracking.spiders.spider_base import SpiderBase

GENERAL_CODE = "utf-8"

class QqBase(SpiderBase):
  name = "qq_base"
  source = "qq"
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


  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  start_urls = [
  ]

  url_filter = "http://v.qq.com/"

  fans_url = "https://om.qq.com/"

  video_list_base = "http://c.v.qq.com/vchannelinfo?otype=json&uin=%s&qm=1&pagenum=%s&num=24"
  base_sub_url = 'http://v.qq.com/x/page/%s.html'
  base_cmt_id_url = 'http://ncgi.video.qq.com/fcgi-bin/video_comment_id?otype=json&op=3&cid=%s&vid=%s'
  base_start_cmt_url = 'http://coral.qq.com/article/%s/comment?orilink=%s'

  def start_requests(self):
    self.start_urls = self.load_entity()
    yield Request(url=self.fans_url, callback=self.parse_fans)
    for url in self.start_urls:
      uid = re.findall('http:\/\/v.qq.com\/vplus\/(.+)', url)[0]
      list_url = self.generate_list_url(uid, 1)
      yield Request(url=list_url, callback=self.parse_list)

  def parse_fans(self, response):
    print response.url
    fans_info = response.xpath('.//a[@class="text-link totalSubscribe"]').xpath('string(.)').extract_first()
    num = re.findall('(\d+)', fans_info)
    fans = ""
    for i in num:
      fans += i
    fans = int(fans)
    ch_url = self.start_urls[0]
    #print fans, self.start_urls[0], self.target_channel
    # fans = int(response.xpath('.//span[@class="num j_rss_count"]').xpath('string(.)').extract_first())
    # ch_url = response.url
    ch = BaseUtil.get_channel(url=ch_url, name=self.target_channel, fans=fans)
    yield ch

  def parse_list(self, response):
    print response.url
    hjson = re.findall('(\{.+\})', response.body)[0]
    hjson = json.loads(hjson, encoding=GENERAL_CODE)
    uid = hjson["euin"]
    if hjson["videolst"] is None:
      return
    for video in hjson["videolst"]:
      uploadtime = video["uploadtime"]
      release = int(QqUtil.format_qq_time(uploadtime))
      topic = video["title"]
      url = video["url"]
      cid = re.findall('\/(\w+)\.htm', url)[0]
      url = self.base_sub_url % cid
      play_count = BaseUtil.convert_playcount(video["play_count"])
      name = self.target_channel
      #print url, release, play_count, topic
      res = self.parse_item(url, name, topic, play_count, release)
      for item in res:
        yield item
    this_page = int(re.findall('pagenum=(\d+)', response.url)[0])
    next_url = self.generate_list_url(uid, this_page + 1)
    yield Request(url=next_url, callback=self.parse_list)

  def parse_item(self, url, name, topic, play_count, release):
    raise NotImplementedError()

  def generate_list_url(self, uid, page):
    return self.video_list_base % (uid, page)

