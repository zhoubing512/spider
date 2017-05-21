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
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, ChannelItem, TrackingItem
from tracking.util.WeiboUtil import WeiboUtil
from tracking.spiders.spider_base import SpiderBase

GENERAL_CODE = "utf-8"


class WeiboBase(SpiderBase):
  name = "weibo_base"
  source = "weibo"
  custom_settings = {
    'ITEM_PIPELINES': {
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
      "tracking.middleware.WeiboCookiesDemoMiddleware": 402,
    },

    'DOWNLOAD_DELAY': 2,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS_PER_IP': 1,
  }

  start_urls = [
  ]

  url_filter = "http://weibo.com"

  base_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&is_all=1&id=100505%s&script_uri=/u/%s&feed_type=0&domain_op=100505&page=%s&pagebar=%s&pre_page=%s"
  fans_base_url = "http://weibo.com/p/100505%s/follow?relate=fans"

  blog_base_url = "http://weibo.com/%s/%s"
  user_base_url = "http://weibo.com/u/%s"
  tag = ""
  page_limit = 200

  keywords = ""

  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # TODO: Load urls from DB

  def parse_weibo_table(self, table, uid):
    blog_url = "get blog url failed"
    try:
      is_repost = table.xpath('.//div[@class="WB_feed_expand"]')
      if len(is_repost) > 0:
        # 这种是转发，包括自己转自己的
        return None
      mid = table.xpath('@mid').extract_first()
      # uid = re.findall('\d+', table.xpath('@tbinfo').extract_first())[0]
      blog_url = self.blog_base_url % (uid, WeiboUtil.mid_to_url(mid))
      content = table.xpath('.//div[@node-type="feed_list_content"]').xpath('string(.)').extract_first()
      content = WeiboUtil.text_clean(content)
      media_box = table.xpath('.//div[@class="media_box"]')
      if len(media_box) > 0:  # 确定该微博是视频
        flash_box = media_box.xpath('./ul/li')
        flash_info = flash_box.xpath('@action-data').extract_first()
        if flash_info is None:
          return None
        play_count = re.findall('play_count=(\d+.?)', flash_info)
        if len(play_count) == 0:
          return None  # 这条微博是图片，不是视频
        play_count = WeiboUtil.convert_playcount(play_count[0])
        mid_info = re.findall('current_mid=(\d+)', flash_info)
        if len(mid_info) == 0:  # 不知道什么情况，反正没有视频
          return None
        current_mid = mid_info[0]
        current_uid = table.xpath('.//div[@class="WB_info"]/a/@usercard').extract_first()
        current_uid = re.findall('id=(\d+)', current_uid)[0]

        duration = re.findall('duration=(\d+)', flash_info)[0]
        bottom_line = table.xpath('.//span[@class="line S_line1"]')
        if mid == current_mid and uid == current_uid:  # 表示该视频是原创而非转发或点赞
          data_read = int(self.get_line_data(bottom_line[0]))  # 读
          data_rpc = int(self.get_line_data(bottom_line[1]))  # 转
          data_cmc = int(self.get_line_data(bottom_line[2]))  # 评
          data_vote = int(self.get_line_data(bottom_line[3]))  # 赞
          release = int(table.xpath('.//a[@node-type="feed_list_item_date"]/@date').extract_first()) / 1000
          # user_name = str(table.xpath('.//div[@class="WB_info"]').xpath('string(.)').extract_first())
          # user_name = WeiboUtil.text_clean(user_name)
          user_name = self.target_channel
          ts = WeiboUtil.date_time_now()
          topic = WeiboUtil.text_clean(content)
          if (self.keywords != "") and (self.keywords not in topic):
            return None
          img = table.xpath('.//div[@node-type="fl_h5_video_pre"]/img/@src').extract_first()
          # print mid, blog_url, play_count, data_read, data_rpc, data_cmc, data_vote, duration, content
          return blog_url, topic, play_count, release, user_name, data_read, data_cmc, user_name, ts, img
    except Exception, e:
      print e, ":", blog_url
    return None

  def parse_next_page(self, data_html, uid, this_page):
    result = []
    next_page_info = data_html.xpath('//div[@node-type="feed_list_page"]').extract_first()
    if (next_page_info is not None) and ('下一页' in next_page_info) and (this_page < self.page_limit):
      url_group = self.generate_time_line_group(uid, page=this_page + 1)
      for url in url_group:
        result.append(url)
    return result

  def get_line_data(self, line):
    line_data = re.findall('\d+', line.xpath('string(.)').extract_first())
    if len(line_data) > 0:
      return line_data[0]
    else:
      return 0

  def generate_time_line_url(self, uid, page, page_bar, pre_page):
    return self.base_url % (uid, uid, page, page_bar, pre_page)

  def generate_time_line_group(self, uid, page):
    return [
      self.generate_time_line_url(uid, page, 0, 0),
      self.generate_time_line_url(uid, page, 0, page),
      self.generate_time_line_url(uid, page, 1, page),
    ]

