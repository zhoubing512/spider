# -*- coding: utf-8 -*-
import re
import time
import datetime
from BaseUtil import BaseUtil


class MiaopaiUtil(BaseUtil):
  def __init__(self):
    BaseUtil.__init__(self)

  @staticmethod
  def get_miaopai_time(release_html):
    r_0 = re.findall('(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', release_html)
    r = re.findall('(\d{2}-\d{2})', release_html)
    r_1 = re.findall('(\d{2}:\d{2})', release_html)
    now = datetime.datetime.now()
    release = 0
    if re.findall(u'分钟', release_html):
      t1t = int(re.findall("\d+", release_html)[0])
      t1 = now + datetime.timedelta(minutes=-t1t)
      release = int(time.mktime(t1.timetuple()))
    elif re.findall(u'小时', release_html):
      t1t = int(re.findall("\d+", release_html)[0])
      t1 = now + datetime.timedelta(hours=-t1t)
      release = int(time.mktime(t1.timetuple()))
    elif "昨天" in release_html:
      yesterday_time = datetime.datetime.now() + datetime.timedelta(days=-1)
      yesterday_time = yesterday_time.strftime('%Y-%m-%d')
      release = int(time.mktime(time.strptime(yesterday_time, '%Y-%m-%d')))
    elif len(r_0) > 0: # YYYY-mm-dd HH:MM
      release = int(time.mktime(time.strptime(r_0[0], '%Y-%m-%d %H:%M')))
    elif len(r) > 0:  # mm-dd
      r_t = str(datetime.datetime.now().year) + "-" + r[0]
      release = int(time.mktime(time.strptime(r_t, '%Y-%m-%d')))
      if release > BaseUtil.date_time_now():
        r_t = str(datetime.datetime.now().year - 1) + "-" + r[0]
        release = int(time.mktime(time.strptime(r_t, '%Y-%m-%d')))
    elif len(r_1) > 0:
      n = datetime.datetime.now()
      r_1 = "%s-%s-%s %s" % (n.year, n.month, n.day, r_1[0])
      release = int(time.mktime(time.strptime(r_1, '%Y-%m-%d %H:%M')))
    return release
