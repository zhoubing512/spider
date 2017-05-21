# encoding=utf-8


import json
import urllib2
import random
import logging
import requests
from util.BaseUtil import BaseUtil
from spiders.spider_base import SpiderBase


class CookieMiddleware(object):

  cookie_base = "http://csr.zintow.com"

  live_time = 60
  last_time = 0
  current_cookie = dict()
  current_cookie_id = ""

  def process_request(self, request, spider):
    if isinstance(spider, SpiderBase):
      self.cookie_base = spider.settings['ACCOUNT_URL']
      t = BaseUtil.date_time_now()
      if t - self.last_time > self.live_time:
        self.last_time = t
        source = spider.source
        target_channel = spider.target_channel
        url = self.generate_cookie_url(source, target_channel)
        self.get_cookie(url)
      request.cookies = self.current_cookie
      request.meta["cookie_id"] = self.current_cookie_id

  def get_cookie(self, url):
    req = urllib2.Request(url)
    data = self.get_response(req)
    logging.info("get cookie: %s" % data)
    if len(data["data"]) > 0:
      valid_cookie = []
      for cookie in data["data"]:
        if cookie["isValid"]:
          valid_cookie.append(cookie)
      the_chosen_one = random.choice(valid_cookie)
      self.current_cookie = BaseUtil.cookie2dict(the_chosen_one["cookie"])
      self.current_cookie_id = the_chosen_one["id"]

  def get_response(self, req):
    res = urllib2.urlopen(req)
    html = res.read()
    hjson = json.loads(html)
    return hjson

  def generate_cookie_url(self, source, channel):
    return self.cookie_base + ("/account/account/%s/domain/%s/identities" % (channel, source))

