import re
import time
import datetime
from BaseUtil import BaseUtil


class WeiboUtil(BaseUtil):
  def __init__(self):
    BaseUtil.__init__(self)

  @staticmethod
  def format_sina_time(ts):
    now = datetime.datetime.now()
    if re.findall(u'\d+\u5206\u949f\u524d', ts):
      t1t = int(re.findall("\d+", ts)[0])
      t1 = now + datetime.timedelta(minutes=-t1t)
      return time.mktime(t1.timetuple())
    if re.findall(u'\u4eca\u5929 \d\d:\d\d', ts):
      t2t = re.findall("\d\d:\d\d", ts)[0]
      t2 = datetime.datetime.strptime(t2t, '%H:%M') \
        .replace(year=now.year, month=now.month, day=now.day)
      return time.mktime(t2.timetuple())
    if re.findall("\d\d\d\d-\d\d-\d\d \d\d:\d\d", ts):
      t4 = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M')
      return time.mktime(t4.timetuple())
    if re.findall("\d\d-\d\d \d\d:\d\d", ts):
      t3 = datetime.datetime.strptime(ts, '%m-%d %H:%M').replace(year=now.year)
      return time.mktime(t3.timetuple())
    if re.findall("\w+ \w+ \d+ \d+:\d+:\d+", ts):
      t5 = re.sub('\+\d{4} ', "", ts)
      ut5 = time.mktime(datetime.datetime.strptime(t5, '%a %b %d %H:%M:%S %Y').timetuple())
      return ut5

  ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

  @staticmethod
  def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
      return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
      rem = num % base
      num = num // base
      arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

  @staticmethod
  def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
      power = (strlen - (idx + 1))
      num += alphabet.index(char) * (base ** power)
      idx += 1

    return num

  @staticmethod
  def mid_to_url(midint):

    midint = str(midint)[::-1]
    size = len(midint) / 7 if len(midint) % 7 == 0 else len(midint) / 7 + 1
    result = []
    for i in range(size):
      s = midint[i * 7: (i + 1) * 7][::-1]
      s = WeiboUtil.base62_encode(int(s))
      s_len = len(s)
      if i < size - 1 and len(s) < 4:
        s = '0' * (4 - s_len) + s
      result.append(s)
    result.reverse()
    return ''.join(result)

  @staticmethod
  def url_to_mid(url):
    url = str(url)[::-1]
    size = len(url) / 4 if len(url) % 4 == 0 else len(url) / 4 + 1
    result = []
    for i in range(size):
      s = url[i * 4: (i + 1) * 4][::-1]
      s = str(WeiboUtil.base62_decode(str(s)))
      s_len = len(s)
      if i < size - 1 and s_len < 7:
        s = (7 - s_len) * '0' + s
      result.append(s)
    result.reverse()
    return int(''.join(result))
