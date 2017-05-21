# -*- coding: utf-8 -*-

import json
import time
import logging
import urllib2
import requests
from BaseUtil import BaseUtil


class TrackingUtil(BaseUtil):
  @staticmethod
  def load_entity(entity_url, target_channel, url_filter=""):
    eu = entity_url + "&name=" + target_channel
    data = BaseUtil.parse_response(url=eu)
    channel_url = []
    for url in data["data"][0]["urls"]:
      if url_filter in url:
        channel_url.append(str(url))
    static_tags = data["data"][0]["tags"]
    return channel_url, static_tags

# unit test
if __name__ == '__main__':
  ch, tag = TrackingUtil.load_entity(entity_url="http://csr.zintow.com/entity/channel?limit=200000000",
                                 target_channel="好好吃",
                                 url_filter="http://www.acfun.cn")
  print tag
  for t in tag:
    print t
  for url in ch:
    print url
