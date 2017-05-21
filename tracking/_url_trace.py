# -*- coding: utf-8 -*-
import time
from tracking.items import TrackingItem
from tracking.pipelineMonitor import MonitorPipeline

class url_trace():
  def load(self):
    mp = MonitorPipeline()

    with open("url.csv", 'r') as f:
      for row in f:
        r = row.split(' ')
        ts = int(time.mktime(time.strptime(r[0], '%Y-%m-%d')))
        print ts, r[1]
        tk = TrackingItem()
        tk["id"] = r[1]
        tk["channel"] = u"好好吃"
        tk["sources"] = "miaopai"
        tk["release"] = ts
        mp.add_topic(tk)
    mp.get_plan()
    mp.add_plan()
    mp.get_plan()
    mp.get_tracker()
    mp.add_tracker()

if __name__ == '__main__':
  tr = url_trace()
  tr.load()
