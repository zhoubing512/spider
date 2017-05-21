# -*- coding: utf-8 -*-

import json
import time
import logging
import urllib2
import requests
from tracking.items import TrackingItem

# TODO: 如果不同平台的channel中文名不同，目前还没有update新的中文名到tags中的功能
class MonitorPipeline(object):
  plan_api = "http://csr.zintow.com/tracking/plan?limit=200000000"
  tracker_api = "http://csr.zintow.com/tracking/tracker?limit=200000000"
  plan_per_day = {}
  url_per_day = {}
  url_dup = set()
  tracker_all = set()
  plan_added = 0
  tracker_added = 0
  tracker_dup = 0

  def close_spider(self, spider):
    self.plan_api = spider.settings['PLAN_URL']
    self.tracker_api = spider.settings['TRACKING_URL']
    logging.info('------------------------ plan_api %s' % self.plan_api)
    logging.info('------------------------ tracker_api %s' % self.tracker_api)
    logging.info("spider[%s] is closing..." % spider.source)
    self.get_plan()
    self.add_plan()
    self.get_plan()
    self.get_tracker()
    self.add_tracker()
    logging.info("plan_added %s" % self.plan_added)
    logging.info("tracker_added %s" % self.tracker_added)
    logging.info("tracker_dup %s" % self.tracker_dup)

  def process_item(self, item, spider):
    if isinstance(item, TrackingItem):
      self.add_topic(item)
    return item

  # 从爬虫中记录topic
  def add_topic(self, tk):
    if not isinstance(tk, TrackingItem):
      return
    if tk["id"] in self.url_dup:
      return
    self.url_dup.add(tk["id"])
    cts = int(tk["release"])
    cts_day = self.ts2dt(cts)
    if cts_day not in self.url_per_day:
      self.url_per_day[cts_day] = []
    self.url_per_day[cts_day].append(tk)

  def add_plan(self):
    for day in self.url_per_day:

      url_sort = self.url_per_day[day]
      url_sort.sort(key=lambda k: (k.get('release', 0)))
      leak = 0
      if day not in self.plan_per_day:
        logging.info("%s not in" % day)
        leak = len(self.url_per_day[day])
        sn = 0
      else:
        leak = len(self.url_per_day[day]) - len(self.plan_per_day[day])
        sn = len(self.plan_per_day[day])
      # 将缺少的plan补齐
      for i in range(0, leak):
        sn += 1
        self.plan_added += 1
        plan = dict()
        plan["name"] = str("好好吃 " + str(day) + " " + str(sn))
        channel = url_sort[i]["channel"]
        plan["tags"] = [channel]
        plan["publishTime"] = int(url_sort[i]["release"]) * 1000 + i
        body = json.dumps(plan)
        self.post_plan(body)

  def get_plan(self):
    req = urllib2.Request(self.plan_api)
    data = self.get_response(req)
    self.plan_per_day = {}
    for plan in data["data"]:
      cts = 0
      if plan["publishTime"] is not None:
        cts = plan["publishTime"] / 1000
      cts_day = self.ts2dt(cts)
      if cts_day not in self.plan_per_day:
        self.plan_per_day[cts_day] = []
      self.plan_per_day[cts_day].append(plan)

  def post_plan(self, plan_body):
    send_pic = requests.post(self.plan_api,
                             data=plan_body,
                             headers={'Content-Type': 'application/json'})
    logging.debug("post_plan %s" % send_pic.content)

  def get_tracker(self):
    req = urllib2.Request(self.tracker_api)
    data = self.get_response(req)
    for tracking in data["data"]:
      self.tracker_all.add(tracking["url"])
    logging.debug('%d %s' % (len(self.tracker_all), self.tracker_all))

  def add_tracker(self):
    for day in self.url_per_day:
      if day not in self.plan_per_day:
        logging.info("%s error" % day)
        continue
      # 只是为了排序
      url_sort = self.url_per_day[day]
      url_sort.sort(key=lambda k: (k.get('release', 0)))
      plan_sort = self.plan_per_day[day]
      plan_sort.sort(key=lambda k: (k.get('publishTime', 0)))
      # ------------
      for i in range(0, len(url_sort)):
        try:
          topic = url_sort[i]
          plan_id = plan_sort[i]["id"]
          # TODO: url去重
          if topic["id"] in self.tracker_all:
            self.tracker_dup += 1
            continue  # 重复的url
          self.tracker_added += 1
          tracker = dict()
          tracker["url"] = topic["id"]
          plan = dict()
          plan["id"] = plan_id
          plan["key"] = plan_id
          tracker["plan"] = plan
          body = json.dumps(tracker)
          self.post_tracker(body)
        except Exception as e:
          logging.info("add_tracker except: %s" % e)

  def post_tracker(self, tracker_body):
    send_pic = requests.post(self.tracker_api,
                             data=tracker_body,
                             headers={'Content-Type': 'application/json'})
    logging.debug("post_tracker %s" % send_pic.content)

  def get_response(self, req):
    res = urllib2.urlopen(req)
    html = res.read()
    hjson = json.loads(html)
    return hjson

  # 时间戳转日期
  def ts2dt(self, ts):
    t = time.localtime(ts)
    return time.strftime('%Y-%m-%d', t)

  # 日期转时间戳
  def dt2ts(self, dt):
    return int(time.mktime(time.strptime(dt, '%Y-%m-%d')))

# unit test
if __name__ == '__main__':
  tc1 = TrackingItem()
  tc1["id"] = "http://test.html_1"
  tc1["channel"] = u"不好吃"
  tc1["sources"] = "test"
  tc1["release"] = 1176768000

  tc2 = TrackingItem()
  tc2["id"] = "http://test.html_2"
  tc2["channel"] = u"不好吃"
  tc2["sources"] = "test"
  tc2["release"] = 1176768000

  mp = MonitorPipeline()
  mp.add_topic(tc1)
  mp.add_topic(tc2)
  mp.get_plan()
  mp.add_plan()
  mp.get_plan()
  mp.get_tracker()
  mp.add_tracker()
