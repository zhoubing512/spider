# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import datetime
import scrapy
import logging
import urllib
import requests
from scrapy.http import Request
from scrapy.spiders import Spider
from tracking.util.TrackingUtil import TrackingUtil

GENERAL_CODE = "utf-8"

class SpiderBase(Spider):
  name = "spider_base"
  source = "spider_base"

  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')
    #self.entity_channel = self.settings['ENTITY_URL']
    #print self.entity_channel

  entity_url = ""
  target_channel = ""
  url_filter = ""
  static_tags = []

  cookie_base = "http://127.0.0.1:8080"

  def load_entity(self):
    self.cookie_base = self.settings['ACCOUNT_URL']
    self.entity_url = self.settings['ENTITY_URL']
    self.target_channel = urllib.unquote(self.settings['TARGET_CHANNEL'])
    urls, self.static_tags = TrackingUtil.load_entity(self.entity_url, self.target_channel, self.url_filter)
    return urls

  def delete_cookie(self, response):
    cookie_id = response.meta["cookie_id"]
    if cookie_id is None:
      return False
    logging.info("Warning: delete cookie %s", cookie_id)
    url = self.cookie_base + ("/account/identity/%s" % cookie_id)
    requests.delete(url)
    return True
