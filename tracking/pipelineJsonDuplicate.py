# -*- coding: utf-8 -*-
import csv
import datetime
import logging
import urllib2
import requests
import codecs
import pymongo
import re
import json
from util.BaseUtil import BaseUtil
from pipelineJson import JsonPipeline
from tracking.items import PlaycountDuplicateItem, TopicDuplicateItem


def log(ut, suffix):
  logging.info(('Update ' if ut == 1 else 'Insert ') + suffix)

PLAYCOUNT_FILE_NAME = 'playcount.%s.%s.json'

class JsonDupelicatePipeline(JsonPipeline):
  forbidden_api = ""

  playcount_duplicate = []
  topic_duplicate = []
  ref_dup_remote = set()
  ref_dup_local = set()

  def __init__(self):
    JsonPipeline.__init__(self)

  def process_item(self, item, spider):
    if item is not None:
      item['sources'] = spider.source
    if isinstance(item, PlaycountDuplicateItem):
      self.append_playcount_duplicate(item)
    if isinstance(item, TopicDuplicateItem):
      self.append_topic_duplicate(item)
    return item

  def close_spider(self, spider):
    self.forbidden_api = spider.settings['FORBIDDEN_URL']
    self.get_forbidden()  # get forbidden urls
    self.process_playcount_duplicate()
    self.process_topic_duplicate()
    self.savePlaycountToFile(spider.source)
    self.saveTopicToFile(spider.source)

  def append_playcount_duplicate(self, item):
    self.playcount_duplicate.append(item)

  def append_topic_duplicate(self, item):
    self.topic_duplicate.append(item)

  def process_playcount_duplicate(self):
    self.ref_dup_local = set()
    self.playcount_duplicate.sort(key=lambda k: (k.get('release', 0)))
    for pcd in self.playcount_duplicate:
      if self.check_and_update_duplicate(url=pcd["id"], key=pcd["key"]):
        continue
      pc = BaseUtil.get_playcount(url=pcd["id"], channel=pcd["channel"], playcount=pcd["playcount"], release=pcd["release"], ts=pcd["ts"])
      pc["sources"] = pcd["sources"]
      self.playcount.append(pc)

  def process_topic_duplicate(self):
    self.ref_dup_local = set()
    self.topic_duplicate.sort(key=lambda k: (k.get('release', 0)))
    for tpd in self.topic_duplicate:
      if self.check_and_update_duplicate(url=tpd["id"], key=tpd["key"]):
        continue
      tp = BaseUtil.get_topic(url=tpd["id"], topic=tpd["topic"], channel=tpd["channel"], playcount=tpd["playcount"],
                              release=tpd["release"], ts=tpd["ts"])
      tp["sources"] = tpd["sources"]
      self.topic.append(tp)

  def check_and_update_duplicate(self, url, key):
    res = False
    if url in self.ref_dup_remote:
      print "found forbidden url in remote:", url, key
      res = True
    elif key in self.ref_dup_local:
      print "found dup url in local:", url, key
      self.post_forbidden(url)  # add dup ref
      res = True
    self.ref_dup_local.add(key)
    return res

  def get_forbidden(self):
    try:
      req = urllib2.Request(self.forbidden_api)
      data = self.get_response(req)
      self.plan_per_day = {}
      for forbidden in data["data"]:
        self.ref_dup_remote.add(forbidden["url"])
    except Exception as e:
      logging.info("JsonDupelicatePipeline.get_forbidden %s" % e)

  def post_forbidden(self, url):
    try:
      forbidden = dict()
      forbidden["url"] = url
      body = json.dumps(forbidden)
      send_pic = requests.post(self.forbidden_api,
                               data=body,
                               headers={'Content-Type': 'application/json'})
      logging.debug("post_forbidden %s" % send_pic.content)
    except Exception as e:
      logging.info("JsonDupelicatePipeline.get_forbidden %s" % e)

  def get_response(self, req):
    res = urllib2.urlopen(req)
    html = res.read()
    hjson = json.loads(html)
    return hjson

# unit test
if __name__ == '__main__':
  dp = JsonDupelicatePipeline()
  dp.post_forbidden("miaowu")
  dp.get_forbidden()
  print dp.ref_dup_remote

