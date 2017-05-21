# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import datetime
import scrapy
import logging
from scrapy import Selector
from urlparse import urljoin
from scrapy.http import Request
from scrapy.spiders import Spider
from tracking.util.BaseUtil import BaseUtil
from tracking.util.TrackingUtil import TrackingUtil
from tracking.spiders.spider_base import SpiderBase
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, RankingItem

GENERAL_CODE = "utf-8"

class MeipaiBase(SpiderBase):
  source = "meipai"
  allowed_domains = ['meipai.com']
  start_urls = []
  url_filter = "meipai.com"
  base_domain_url = "http://www.meipai.com"
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
    logging.info("Start to crawl from Meipai")

  def start_requests(self):
    self.start_urls = self.load_entity()
    for channel_url in self.start_urls:
      logging.info('# # # Meipai channel url: %s' % channel_url)
      requests = self.loadRequest(channel_url)
      for request in requests:
        yield request

  def parse_url(self,response):
    nextPageObj = response.xpath('//a[@class="paging-next dbl"]')
    if len(nextPageObj) == 1:
      href = nextPageObj.xpath('@href').extract_first()
      nextPageUrl = urljoin(self.base_domain_url, href)
      yield Request(nextPageUrl, callback = self.parse_url)
    ul = response.xpath('//*[@id="mediasList"]/li')
    for li in ul:
      video_link_part = str(li.xpath('./a/meta[@content]').extract_first())
      link_part = re.findall('/media/\d+', video_link_part)[0]
      video_link = urljoin(self.base_domain_url, link_part)
      yield Request(video_link, callback = self.parse_indicators)

  def parse_indicators(self, response):
    id = response.url
    channel_str = response.xpath('//*[@id="mediaUser"]/div/h3[@class="detail-name pa"]/a/text()').extract_first()
    channel_part = str(BaseUtil().text_clean(channel_str)).decode('utf-8')

    rl = response.xpath('//div[@class="detail-time pa"]/strong/text()').extract_first().strip()
    rl_hour = re.findall('\d{2}:\d{2}', rl)
    rl_content = response.xpath('/html/head/meta[11][@content]').extract_first()
    rl_year= re.findall('\d{4}-\d{2}-\d{2}', rl_content)[0]
    time_str = str(''.join(rl_year)+' '+''.join(rl_hour)+':00')
    release = int(time.mktime(time.strptime(time_str,"%Y-%m-%d %H:%M:%S")))
    topic_str = response.xpath('//h1[@class="detail-description break js-convert-emoji"]').xpath('string(.)').extract_first()
    topic = BaseUtil().text_clean(topic_str)

    playcount_part = response.xpath('//div[@class="detail-location"]/text()').extract()[1]
    playcount_list = re.findall('\d+', playcount_part)

    playcount = 0
    if len(playcount_list) > 0:
      playcount = int(playcount_list[0])

    upcount_part = response.xpath('//span[@class="pr top-2"]/text()').extract_first()
    upcount_part_list = re.findall('\d+', upcount_part)
    upcount = 0
    if len(upcount_part_list) > 0:
      upcount = int(upcount_part_list[0])

    repostc_part = response.xpath('//*[@id="repostMediaBtn"]/text()').extract()[1]
    repostc_part_list = re.findall('\d+', repostc_part)
    repost = 0
    if len(repostc_part_list) > 0:
      repost = int(repostc_part_list[0])

    commentcount_part = response.xpath('//*[@id="commentCount"]/text()').extract_first()
    commentcount_part_list = re.findall('\d+', commentcount_part)
    commentcount = 0
    if len(commentcount_part_list) > 0:
      commentcount = int(commentcount_part_list[0])
    items = self.loadItems(id, topic, playcount, release, repost, commentcount, upcount)
    for item in items:
      yield item

  def loadRequest(self, url):
    raise NotImplementedError()

  def loadItems(self, url, topic, playcount, release, repost, commentcount, upcount):
    raise NotImplementedError()
