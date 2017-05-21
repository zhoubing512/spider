# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

# 跟踪系统专用，不会写入json文件中
class TrackingItem(Item):
  id = Field()  #  视频或文章的URL
  sources = Field()  # 视频或文章所在平台，如"微博"，一般使用该平台的域名，如"weibo"
  channel = Field()  # 公众号名称，如"好好吃"
  release = Field()  # 视频或文章发布时间

# 主题
class TopicItem(Item):
  id = Field()
  sources = Field()
  channel = Field()
  playcount = Field()  # 播放数
  release = Field()
  topic = Field()  # 视频或文章标题
  ts = Field()  # 数据抓取时间
  category = Field() # 内容类型 video article

# 主题 微博单独使用的数据结构
class TopicDuplicateItem(Item):
  id = Field()
  sources = Field()
  channel = Field()
  playcount = Field()
  release = Field()
  topic = Field()
  ts = Field()
  key = Field()  # 微博会发布重复的视频(炒冷饭)，key用来去重(key的值为秒拍的视频URL)
  category = Field()

# 推荐数
class RecommendationItem(Item):
  id = Field()
  sources = Field()
  recommendationCount = Field()  # 推荐数
  ts = Field()
  category = Field()

# 转发数
class RepostItem(Item):
  id = Field()
  sources = Field()
  repostCount = Field()  # 转发数
  ts = Field()
  category = Field()

# 评论数
class CommentsCountItem(Item):
  id = Field()
  sources = Field()
  channel = Field()
  count = Field()  # 评论数
  ts = Field()
  category = Field()

# 浏览数
class PageviewItem(Item):
  id = Field()
  sources = Field()
  view = Field()  # 浏览数
  ts = Field()
  category = Field()

# 播放时长
class DurationItem(Item):
  id = Field()
  sources = Field()
  duration = Field()  # 播放时长单位为秒
  ts = Field()
  category = Field()

# 播放次数+用户+发布时间
class PlaycountItem(Item):
  id = Field()
  sources = Field()
  playcount = Field()  # 播放次数
  channel = Field()
  release = Field()  # 发布时间
  ts = Field()
  category = Field()

# 播放次数+用户+发布时间 微博单独使用的数据结构
class PlaycountDuplicateItem(Item):
  id = Field()
  sources = Field()
  playcount = Field()
  channel = Field()
  release = Field()
  ts = Field()
  key = Field()  # 微博会发布重复的视频 key用来去重(key的值为秒拍的视频URL)
  category = Field()

# 赞数
class UpCountItem(Item):
  id = Field()
  sources = Field()
  count = Field()  # 赞数
  ts = Field()
  category = Field()

# 踩数
class DownCountItem(Item):
  id = Field()
  sources = Field()
  count = Field() # 踩数
  ts = Field()
  category = Field()

# 收藏数
class CollectionCountItem(Item):
  id = Field()
  sources = Field()
  count = Field()  # 收藏数
  ts = Field()
  category = Field()

# 用户粉丝信息
class ChannelItem(Item):
  id = Field()
  sources = Field()
  name = Field()  # 公众号名称 如"好好吃"
  fans = Field()  # 用户粉丝信息
  ts = Field()

# 话题排行榜(目前只有微博使用该数据)
class RankingItem(Item):
  sources = Field()
  rank = Field()  # 话题的排名
  name = Field()  # 话题的名字
  index = Field()  # 搜索指数
  species = Field()  # 话题的领域
  ts = Field()

# 大V排行榜(目前只有微博使用该数据)
class BigVItem(Item):
  sources = Field()
  rank = Field()  # 大v的排名
  name = Field()  # 大v的名字
  index = Field()  # 搜索指数
  species = Field()  # 大v的领域
  ts = Field()

# toutiao weekly analysis
class AnalysisItem(Item):
  id = Field()
  sources = Field()
  topic = Field()
  progress = Field()  # 平均播放进度
  bounce = Field()  # 跳出率
  playtime = Field()  # 平均播放时长 单位秒
