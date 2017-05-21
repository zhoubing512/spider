import re
import time
import datetime
from BaseUtil import BaseUtil


class YoukuUtil(BaseUtil):
  def __init__(self):
    BaseUtil.__init__(self)

  @staticmethod
  def format_youku_time(ts):
    now = datetime.datetime.now()
    if re.findall(u'\d+\u5206\u949f\u524d', ts): # x minutes ago
      tmt = int(re.findall("\d+", ts)[0])
      tm = now + datetime.timedelta(minutes=-tmt)
      return time.mktime(tm.timetuple())
    if re.findall(u'\d+\u5c0f\u65f6\u524d', ts): # x hours age
      tht = int(re.findall("\d+", ts)[0])
      th = now + datetime.timedelta(hours=-tht)
      return time.mktime(th.timetuple())
    if re.findall(u'\u4eca\u5929 \d\d:\d\d', ts): # today
      ttt = re.findall("\d\d:\d\d", ts)[0]
      tt = datetime.datetime.strptime(ttt, '%H:%M') \
        .replace(year=now.year, month=now.month, day=now.day)
      return time.mktime(tt.timetuple())
    if re.findall(u'\u6628\u5929 \d\d:\d\d', ts): # yesterday
      tyt = re.findall("\d\d:\d\d", ts)[0]
      ty = datetime.datetime.strptime(tyt, '%H:%M') \
        .replace(year=now.year, month=now.month, day=(now + datetime.timedelta(days=-1)).day)
      return time.mktime(ty.timetuple())
    if re.findall(u'\u524d\u5929 \d\d:\d\d', ts): # the day before yesterday
      tbyt = re.findall("\d\d:\d\d", ts)[0]
      tby = datetime.datetime.strptime(tbyt, '%H:%M') \
        .replace(year=now.year, month=now.month, day=(now + datetime.timedelta(days=-2)).day)
      return time.mktime(tby.timetuple())
    if re.findall(u'\d+\u5929\u524d', ts): # x days ago
      txdt = int(re.findall("\d+", ts)[0]) + 1
      txd = now + datetime.timedelta(days=-txdt)
      return time.mktime(txd.timetuple())
    if re.findall("\d\d\d\d-\d\d-\d\d \d\d:\d\d", ts):
      t4 = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M')
      return time.mktime(t4.timetuple())
    if re.findall("\d\d\d\d-\d\d-\d\d", ts):
      t6 = datetime.datetime.strptime(ts, '%Y-%m-%d')
      return time.mktime(t6.timetuple())
    if re.findall("\d\d-\d\d \d\d:\d\d", ts):
      t3 = datetime.datetime.strptime(ts, '%m-%d %H:%M').replace(year=now.year)
      return time.mktime(t3.timetuple())
    if re.findall("\w+ \w+ \d+ \d+:\d+:\d+", ts):
      t5 = re.sub('\+\d{4} ', "", ts)
      ut5 = time.mktime(datetime.datetime.strptime(t5, '%a %b %d %H:%M:%S %Y').timetuple())
      return ut5
