import urllib2
import datetime
import time
import json
import logging

class ProxyScanner(object):
  header = {
      'User-Agent': "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",

  }
  free_target_url = "http://fetcher.zintow.com:8000/?count=200&types=0"
  xun_target_url = "http://ops.zintow.com/ipproxy/iplist"
  #xun_target_url = "http://172.16.0.110/ipproxy/iplist"

  live_time = 30
  proxies = []

  def __init__(self):
    self.__last_time = 0

  def check_and_get_proxies_json(self, url, jsontype='default'):
    t = self.__get_time()
    if t - self.__last_time > self.live_time:
      self.__last_time = t
      self.__get_proxies_json(url, jsontype)

  def __get_proxies_json(self, url, jsontype):
    try:
      self.proxies = []
      req = urllib2.Request(url, headers=self.header)
      res = urllib2.urlopen(req)
      html = res.read()
      hjson = json.loads(html)
      if jsontype.lower() == 'xun_proxy':
        for pro in hjson:
          try:
            errcode = pro["ERRORCODE"]
            if errcode != "0":
              continue
            print pro
            proxy = str("http://%s:%s" % (pro['RESULT']["wanIp"], str(pro['RESULT']["proxyport"])))
            self.proxies.append(proxy)
          except Exception as e:
            logging.error("[proxy] get_proxies Exception: %s" % str(e))
      else:
        for pro in hjson:
          proxy = str("http://%s:%s" % (pro["ip"], str(pro["port"])))
          self.proxies.append(proxy)
      logging.info("[proxy] get proxies, count:%s" % len(self.proxies))
    except Exception as e:
      logging.error("[proxy] get_proxies Exception: %s" % str(e))

  def check_and_get_proxies(self, url):
    t = self.__get_time()
    if t - self.__last_time > self.live_time:
      self.__last_time = t
      self.__get_proxies(url)

  def __get_proxies(self, url):
    try:
      req = urllib2.Request(url, headers=self.header)
      res = urllib2.urlopen(req)
      html = res.read()
      lst = html.split('\n')
      self.proxies = []
      for pro in lst:
        info = pro.split(':')
        if len(info) > 1:
          proxy = str("http://%s:%s" % (info[0], info[1]))
          self.proxies.append(proxy)
          #print proxy
      logging.info("[proxy] get proxies, count:%s" % len(self.proxies))
    except Exception as e:
      logging.error("[proxy] get_proxies Exception:" % str(e))

  def __get_time(self):
    return time.mktime(datetime.datetime.now().timetuple())

# unit test
if __name__ == '__main__':
  ps = ProxyScanner()
  ps.check_and_get_proxies_json(ps.xun_target_url, 'xun_proxy')
  print ps.proxies
