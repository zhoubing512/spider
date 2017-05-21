import re
import md5
import time
import datetime
from BaseUtil import BaseUtil


class ToutiaoUtil(BaseUtil):
  def __init__(self):
    BaseUtil.__init__(self)

  @staticmethod
  def generateAS():
    i = int(time.mktime(datetime.datetime.now().timetuple()))
    t = str('%x' % i).upper()
    m = md5.new()
    m.update(str(i))
    e = str(m.hexdigest()).upper()
    if 8 != len(t) :
      return '479BB4B7254C150'
    s = e[:5]
    o = e[-5:]
    a = ''
    for n in range(5):
      a += s[n] + t[n]
    return 'A1' + a + t[-3:]
