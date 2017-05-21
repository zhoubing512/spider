# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import datetime
import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import Spider
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, RankingItem
from tracking.util.WeiboUtil import WeiboUtil

GENERAL_CODE = "utf-8"

film_key = ["电影", "电视剧", "综艺", "动漫"]
person_key = ["人物"]
entertainment_key = ["娱乐"]
sports_key = ["体育"]
auto_key = ["汽车"]

class BaiduHotSearch(Spider):
  name = "baidu_hot_search_task"
  source = "baidu"
  custom_settings = {
    'ITEM_PIPELINES': {
      'tracking.pipelines.DefaultPipeline': 200,
      'tracking.pipelineJson.JsonPipeline': 301,
    },
    'DOWNLOADER_MIDDLEWARES': {
      "tracking.middleware.UserAgentMiddleware": 401,
    },

    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS_PER_IP': 1,
  }

  start_urls = [
    "http://top.baidu.com/buzz?b=26&c=1&fr=topcategory_c1",  # 今日电影排行榜
    # "http://top.baidu.com/buzz?b=661&c=1&fr=topbuzz_b26_c1",  # 今日热映电影排行榜
    # "http://top.baidu.com/buzz?b=659&c=1&fr=topbuzz_b661_c1",  # 即将上映电影排行榜
    # "http://top.baidu.com/buzz?b=338&c=1&fr=topbuzz_b659_c1",  # 今日爱情电影排行榜
    # "http://top.baidu.com/buzz?b=340&c=1&fr=topbuzz_b338_c1",  # 今日喜剧电影排行榜
    # "http://top.baidu.com/buzz?b=339&c=1&fr=topbuzz_b340_c1",  # 今日惊悚电影排行榜
    # "http://top.baidu.com/buzz?b=437&c=1&fr=topbuzz_b339_c1",  # 今日科幻电影排行榜
    # "http://top.baidu.com/buzz?b=337&c=1&fr=topbuzz_b437_c1",  # 今日剧情电影排行榜

    "http://top.baidu.com/buzz?b=4&c=2&fr=topcategory_c2",  # 今日电视剧排行榜
    # "http://top.baidu.com/buzz?b=349&c=2&fr=topbuzz_b4_c2",  # 今日偶像电视剧排行榜
    # "http://top.baidu.com/buzz?b=350&c=2&fr=topbuzz_b349_c2",  # 今日言情电视剧排行榜
    # "http://top.baidu.com/buzz?b=351&c=2&fr=topbuzz_b350_c2",  # 今日古装电视剧排行榜
    # "http://top.baidu.com/buzz?b=448&c=2&fr=topbuzz_b351_c2",  # 今日家庭伦理剧排行榜
    # "http://top.baidu.com/buzz?b=452&c=2&fr=topbuzz_b448_c2",  # 今日美剧排行榜
    # "http://top.baidu.com/buzz?b=453&c=2&fr=topbuzz_b452_c2",  # 今日韩剧排行榜
    # "http://top.baidu.com/buzz?b=466&c=2&fr=topbuzz_b453_c2",  # 今日日剧排行榜
    # "http://top.baidu.com/buzz?b=464&c=2&fr=topbuzz_b466_c2",  # 今日港剧排行榜
    # "http://top.baidu.com/buzz?b=465&c=2&fr=topbuzz_b464_c2",  # 今日台剧排行榜
    # "http://top.baidu.com/buzz?b=467&c=2&fr=topbuzz_b465_c2",  # 今日泰剧排行榜

    "http://top.baidu.com/buzz?b=19&c=3&fr=topcategory_c3",  # 今日综艺排行榜
    # "http://top.baidu.com/buzz?b=439&c=3&fr=topbuzz_b19_c3",  # 今日访谈综艺排行榜
    # "http://top.baidu.com/buzz?b=440&c=3&fr=topbuzz_b439_c3",  # 今日情感综艺排行榜
    # "http://top.baidu.com/buzz?b=441&c=3&fr=topbuzz_b440_c3",  # 今日选秀综艺节目排行榜
    # "http://top.baidu.com/buzz?b=368&c=3&fr=topbuzz_b441_c3",  # 今日内地综艺排行榜
    # "http://top.baidu.com/buzz?b=369&c=3&fr=topbuzz_b368_c3",  # 今日港台综艺排行榜

    "http://top.baidu.com/buzz?b=23&c=5&fr=topcategory_c5",  # 今日动漫卡通排行榜
    # "http://top.baidu.com/buzz?b=442&c=5&fr=topbuzz_b23_c5",  # 今日搞笑动漫排行榜
    # "http://top.baidu.com/buzz?b=443&c=5&fr=topbuzz_b442_c5",  # 今日益智动漫排行榜
    # "http://top.baidu.com/buzz?b=444&c=5&fr=topbuzz_b443_c5",  # 今日冒险动漫排行榜
    # "http://top.baidu.com/buzz?b=623&c=5&fr=topbuzz_b444_c5 ",  # 今日情感动漫排行榜
    # "http://top.baidu.com/buzz?b=445&c=5&fr=topbuzz_b623_c5",  # 今日国产动漫排行榜
    # "http://top.baidu.com/buzz?b=446&c=5&fr=topbuzz_b445_c5",  # 今日日本动漫排行榜
    # "http://top.baidu.com/buzz?b=447&c=5&fr=topbuzz_b446_c5",  # 今日欧美动漫排行榜

    "http://top.baidu.com/buzz?b=258&fr=topcategory_c9",  # 今日热点人物排行榜
    # "http://top.baidu.com/buzz?b=618&c=9&fr=topbuzz_b258",  # 今日娱乐名人排行榜
    # "http://top.baidu.com/buzz?b=18&c=9&fr=topbuzz_b618_c9",  # 今日女演员排行榜
    # "http://top.baidu.com/buzz?b=17&c=9&fr=topbuzz_b18_c9",  # 今日男演员排行榜
    # "http://top.baidu.com/buzz?b=1395&c=9&fr=topbuzz_b17_c9",  # 今日演员排行榜
    # "http://top.baidu.com/buzz?b=16&c=9&fr=topbuzz_b1395_c9",  # 今日女歌手排行榜
    # "http://top.baidu.com/buzz?b=15&c=9&fr=topbuzz_b16_c9",  # 今日男歌手排行榜
    # "http://top.baidu.com/buzz?b=1396&c=9&fr=topbuzz_b15_c9",  # 今日歌手排行榜
    # "http://top.baidu.com/buzz?b=260&c=9&fr=topbuzz_b1396_c9",  # 今日名家人物排行榜
    # "http://top.baidu.com/buzz?b=454&c=9&fr=topbuzz_b260_c9",  # 今日主持人排行榜
    # "http://top.baidu.com/buzz?b=255&c=9&fr=topbuzz_b454_c9",  # 今日体坛人物排行榜
    # "http://top.baidu.com/buzz?b=3&c=9&fr=topbuzz_b255_c9",  # 今日美女排行榜
    # "http://top.baidu.com/buzz?b=22&c=9&fr=topbuzz_b3_c9",  # 今日帅哥排行榜
    # "http://top.baidu.com/buzz?b=493&c=9&fr=topbuzz_b22_c9",  # 今日选秀歌手排行榜
    # "http://top.baidu.com/buzz?b=491&c=9&fr=topbuzz_b493_c9",  # 今日欧美明星排行榜
    # "http://top.baidu.com/buzz?b=261&c=9&fr=topbuzz_b491_c9",  # 今日财经人物排行榜
    # "http://top.baidu.com/buzz?b=257&c=9&fr=topbuzz_b261_c9",  # 今日互联网人物排行榜
    # "http://top.baidu.com/buzz?b=259&c=9&fr=topbuzz_b257_c9",  # 今日历史人物排行榜
    # "http://top.baidu.com/buzz?b=612&c=9&fr=topbuzz_b259_c9",  # 今日公益明星排行榜

    # "http://top.baidu.com/buzz?b=7&c=10&fr=topcategory_c10",  # 今日小说排行榜
    # "http://top.baidu.com/buzz?b=353&c=10&fr=topbuzz_b7_c10",  # 今日玄幻奇幻小说排行榜
    # "http://top.baidu.com/buzz?b=355&c=10&fr=topbuzz_b353_c10",  # 今日都市言情小说排行榜
    # "http://top.baidu.com/buzz?b=354&c=10&fr=topbuzz_b1508_c10",  # 今日武侠仙侠小说排行榜
    # "http://top.baidu.com/buzz?b=1508&c=10&fr=topbuzz_b1509_c10",  # 青春校园
    # "http://top.baidu.com/buzz?b=1509&c=10&fr=topbuzz_b354_c10",  # 穿越架空
    # "http://top.baidu.com/buzz?b=356&c=10&fr=topbuzz_b1509_c10",  # 今日科幻悬疑小说排行榜
    # "http://top.baidu.com/buzz?b=459&c=10&fr=topbuzz_b356_c10",  # 今日历史军事小说排行榜
    # "http://top.baidu.com/buzz?b=1512&c=10&fr=topbuzz_b459_c10",  # 游戏竞技
    # "http://top.baidu.com/buzz?b=1510&c=10&fr=topbuzz_b1512_c10",  # 耽美同人
    # "http://top.baidu.com/buzz?b=1513&c=10&fr=topbuzz_b1510_c10",  # 文学经典

    "http://top.baidu.com/buzz?b=1&c=513&fr=topcategory_c513",  # 实时热点排行榜
    # "http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1_c513",  # 今日热点事件排行榜
    # "http://top.baidu.com/buzz?b=42&c=513&fr=topbuzz_b341_c513",  # 七日热点排行榜
    # "http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513",  # 民生热点排行榜
    "http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513",  # 娱乐热点排行榜
    "http://top.baidu.com/buzz?b=11&c=513&fr=topbuzz_b344_c513",  # 体育热点排行榜

    "http://top.baidu.com/buzz?b=1564&c=18&fr=topcategory_c18",  # 汽车月度榜单

    #"http://top.baidu.com/buzz?b=1566&c=15&fr=topbuzz_b20_c15",  # 手机月度榜单
    #"http://top.baidu.com/buzz?b=20&c=15&fr=topbuzz_b1566_c15",  # 今日软件排行榜
  ]

  ts = WeiboUtil.date_time_now()

  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8')

  def start_requests(self):
    for url in self.start_urls:
      yield Request(url, callback=self.parse)

  def parse(self, response):
    print response.url
    top_title = WeiboUtil.text_clean(response.xpath('//div[@class="top-title"]/h2').xpath('string(.)').extract_first())
    print top_title
    ranking_list = response.xpath('//td[@class="first"]')
    for ranking in ranking_list:
      rank = int(WeiboUtil.text_clean(ranking.xpath('string(.)').extract_first()))
      name = ranking.xpath('../td[@class="keyword"]/a[@class="list-title"]').xpath('text()').extract_first()
      name = WeiboUtil.text_clean(name)
      index = int(WeiboUtil.text_clean(ranking.xpath('../td[@class="last"]').xpath('string(.)').extract_first()))
      if index == '':
        index = ranking.xpath('../td[@class="last"]/div/span/@style').extract_first()
        index = int(re.findall('\d+', index)[0])
      else:
        index = int(index)
      #print rank, name, index
      species = self.identify(top_title)
      rk = RankingItem()
      rk["rank"] = rank
      rk["name"] = name
      rk["index"] = index
      rk["species"] = species
      rk["ts"] = self.ts
      yield rk

  def identify(self, url):
    if "电影" in url:
      return "电影"
    elif "电视剧" in url:
      return "电视剧"
    elif "综艺" in url:
      return "综艺"
    elif "动漫" in url:
      return "动漫"
    elif "人物" in url:
      return "人物"
    elif "娱乐" in url:
      return "娱乐"
    elif "体育" in url:
      return "体育"
    elif "汽车" in url:
      return "汽车"
    return "综合"

