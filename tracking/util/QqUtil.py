import re
import time
import datetime
from BaseUtil import BaseUtil


class QqUtil(BaseUtil):
  @staticmethod
  def format_qq_time(ts):
    now = datetime.datetime.now()
    if re.findall(u'\d+\u5206\u949f\u524d', ts):
      t1t = int(re.findall("\d+", ts)[0])
      t1 = now + datetime.timedelta(minutes=-t1t)
      return time.mktime(t1.timetuple())
    if re.findall(u'\d+\u5c0f\u65f6\u524d', ts):
      t1t = int(re.findall("\d+", ts)[0])
      t1 = now + datetime.timedelta(hours=-t1t)
      return time.mktime(t1.timetuple())
    if re.findall("\d\d\d\d-\d\d-\d\d", ts):
      t4 = datetime.datetime.strptime(ts, '%Y-%m-%d')
      return time.mktime(t4.timetuple())
    return BaseUtil.date_time_now()
