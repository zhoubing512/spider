# -*- coding: utf-8 -*-
import csv
import datetime
import logging
import pymongo
import re
from tracking.items import PageviewItem, CommentsCountItem, TopicItem, PlaycountItem, DurationItem, RecommendationItem, RepostItem
from tracking.items import UpCountItem, DownCountItem, CollectionCountItem, ChannelItem, RankingItem, BigVItem, AnalysisItem

def log(ut, suffix):
  logging.info(('Update ' if ut == 1 else 'Insert ') + suffix)

class DefaultPipeline(object):
  def process_item(self, item, spider):
    logging.debug(item)
    return item

PLAYCOUNT_FILE_NAME = 'playcount.%s.%s.csv'
DURATION_FILE_NAME = 'duration.%s.%s.csv'
PAGEVIEW_FILE_NAME = 'pageview.%s.%s.csv'
COMMENTSCOUNT_FILE_NAME = 'commentscount.%s.%s.csv'
TOPIC_FILE_NAME = 'topic.%s.%s.csv'
RECOMMENDATION_FILE_NAME = 'recommendation.%s.%s.csv'
REPOST_FILE_NAME = 'repost.%s.%s.csv'
UP_FILE_NAME = 'up.%s.%s.csv'
DOWN_FILE_NAME = 'down.%s.%s.csv'
COLLECTION_FILE_NAME = 'collection.%s.%s.csv'
CHANNEL_FILE_NAME = 'channel.%s.%s.csv'
RANKING_FILE_NAME = 'ranking.%s.%s.csv'
BIGV_FILE_NAME = 'bigv.%s.%s.csv'
ANALYSIS_FILE_NAME = 'analysis.%s.%s.csv'

class FilePipeline(object):
  def open_spider(self, spider):
    self.playcount = []
    self.duration = []
    self.pageview = []
    self.commentscount = []
    self.topic = []
    self.recommendation = []
    self.repost = []
    self.up = []
    self.down = []
    self.collection = []
    self.channel = []
    self.ranking = []
    self.bigv = []
    self.analysis = []

  def close_spider(self, spider):
    self.savePlaycountToFile(spider.source)
    self.saveDurationToFile(spider.source)
    self.savePageviewToFile(spider.source)
    self.saveCommentsCountToFile(spider.source)
    self.saveTopicToFile(spider.source)
    self.saveRecommendationToFile(spider.source)
    self.saveRepostToFile(spider.source)
    self.saveUpToFile(spider.source)
    self.saveDownToFile(spider.source)
    self.saveCollectionToFile(spider.source)
    self.saveChannelToFile(spider.source)
    self.saveRankingToFile(spider.source)
    self.saveBigVToFile(spider.source)
    self.saveAnalysisToFile(spider.source)

  def process_item(self, item, spider):
    item['sources'] = spider.source
    if isinstance(item, PlaycountItem):
      return self.storePlaycount(item, spider)
    if isinstance(item, DurationItem):
      return self.storeDuration(item, spider)
    if isinstance(item, PageviewItem):
      return self.storePageview(item, spider)
    if isinstance(item, CommentsCountItem):
      return self.storeCommentscount(item, spider)
    if isinstance(item, TopicItem):
      return self.storeTopic(item, spider)
    if isinstance(item, RecommendationItem):
      return self.storeRecommendation(item, spider)
    if isinstance(item, RepostItem):
      return self.storeRepsot(item, spider)
    if isinstance(item, UpCountItem):
      return self.storeUp(item, spider)
    if isinstance(item, DownCountItem):
      return self.storeDown(item, spider)
    if isinstance(item, CollectionCountItem):
      return self.storeCollection(item, spider)
    if isinstance(item, ChannelItem):
      return self.storeChannel(item, spider)
    if isinstance(item, RankingItem):
      return self.storeRanking(item, spider)
    if isinstance(item, BigVItem):
      return self.storeBigV(item, spider)
    if isinstance(item, AnalysisItem):
      return self.storeAnalysis(item, spider)
    return item

  def storePlaycount(self, item, spider):
    self.playcount.append(item)
    if len(self.playcount) >= int(spider.settings['BUFFER_SIZE']):
      self.savePlaycountToFile(spider.source)

  def storeDuration(self, item, spider):
    self.duration.append(item);
    if len(self.duration) >= int(spider.settings['BUFFER_SIZE']):
      self.saveDurationToFile(spider.source)

  def storePageview(self, item, spider):
    self.pageview.append(item)
    if len(self.pageview) >= int(spider.settings['BUFFER_SIZE']):
      self.savePageviewToFile(spider.source)

  def storeCommentscount(self, item, spider):
    self.commentscount.append(item)
    if len(self.commentscount) >= int(spider.settings['BUFFER_SIZE']):
      self.saveCommentsCountToFile(spider.source)

  def storeTopic(self, item, spider):
    self.topic.append(item)
    if len(self.topic) >= int(spider.settings['BUFFER_SIZE']):
      self.saveTopicToFile(spider.source)
    return item

  def storeRecommendation(self, item, spider):
    self.recommendation.append(item)
    if len(self.recommendation) >= int(spider.settings['BUFFER_SIZE']):
      self.saveRecommendationToFile(spider.source)

  def storeRepsot(self, item, spider):
    self.repost.append(item)
    if len(self.repost) >= int(spider.settings['BUFFER_SIZE']):
      self.saveRepostToFile(spider.source)

  def storeUp(self, item, spider):
    self.up.append(item)
    if len(self.up) >= int(spider.settings['BUFFER_SIZE']):
      self.saveUpToFile(spider.source)

  def storeDown(self, item, spider):
    self.down.append(item)
    if len(self.down) >= int(spider.settings['BUFFER_SIZE']):
      self.saveDownToFile(spider.source)

  def storeCollection(self, item, spider):
    self.collection.append(item)
    if len(self.collection) >= int(spider.settings['BUFFER_SIZE']):
      self.saveCollectionToFile(spider.source)

  def storeChannel(self, item, spider):
    self.channel.append(item)
    if len(self.channel) >= int(spider.settings['BUFFER_SIZE']):
      self.saveChannelToFile(spider.source)

  def storeRanking(self, item, spider):
    self.ranking.append(item)
    if len(self.ranking) >= int(spider.settings['BUFFER_SIZE']):
      self.saveRankingToFile(spider.source)

  def storeBigV(self, item, spider):
    self.bigv.append(item)
    if len(self.bigv) >= int(spider.settings['BUFFER_SIZE']):
      self.saveBigVToFile(spider.source)

  def storeAnalysis(self, item, spider):
    self.analysis.append(item)
    if len(self.analysis) >= int(spider.settings['BUFFER_SIZE']):
      self.saveAnalysisToFile(spider.source)

  def savePlaycountToFile(self, source):
    self.saveToFile(PLAYCOUNT_FILE_NAME, source, self.playcount, ['id', 'sources', 'playcount', 'channel', 'release', 'ts', 'category'], type_name="playcount")
    self.playcount = []

  def saveDurationToFile(self, source):
    self.saveToFile(DURATION_FILE_NAME, source, self.duration, ['id','sources','duration','ts', 'category'], type_name="duration")
    self.duration = []

  def savePageviewToFile(self, source):
    self.saveToFile(PAGEVIEW_FILE_NAME, source, self.pageview, ['id','sources','view','ts', 'category'], type_name="pageview")
    self.pageview = []

  def saveCommentsCountToFile(self, source):
    self.saveToFile(COMMENTSCOUNT_FILE_NAME, source, self.commentscount, ['id','sources','count','ts', 'category'], type_name="commentscount")
    self.commentscount = []

  def saveTopicToFile(self, source):
    self.saveToFile(TOPIC_FILE_NAME, source, self.topic, ['id','sources','topic','ts', 'category'], type_name="topic")
    self.topic = []

  def saveRecommendationToFile(self, source):
    self.saveToFile(RECOMMENDATION_FILE_NAME, source, self.recommendation, ['id','sources','recommendationCount','ts', 'category'], type_name="recommendation")
    self.recommendation = []

  def saveRepostToFile(self, source):
    self.saveToFile(REPOST_FILE_NAME, source, self.repost, ['id','sources','repostCount','ts', 'category'], type_name="repost")
    self.repost = []

  def saveUpToFile(self, source):
    self.saveToFile(UP_FILE_NAME, source, self.up, ['id','sources','count','ts', 'category'], type_name="up")
    self.up = []

  def saveDownToFile(self, source):
    self.saveToFile(DOWN_FILE_NAME, source, self.down, ['id','sources','count','ts', 'category'], type_name="down")
    self.down = []

  def saveCollectionToFile(self, source):
    self.saveToFile(COLLECTION_FILE_NAME, source, self.collection, ['id','sources','count','ts', 'category'], type_name="collection")
    self.collection = []

  def saveChannelToFile(self, source):
    self.saveToFile(CHANNEL_FILE_NAME, source, self.channel, ['id','sources','fans','ts'], type_name="channel")
    self.channel = []

  def saveRankingToFile(self, source):
    self.saveToFile(RANKING_FILE_NAME, source, self.ranking, ['rank','sources','name','index','ts'], type_name="ranking")
    self.channel = []

  def saveBigVToFile(self, source):
    self.saveToFile(BIGV_FILE_NAME, source, self.bigv, ['rank','sources','name','index','ts'], type_name="bigv")
    self.bigv = []

  def saveAnalysisToFile(self, source):
    self.saveToFile(ANALYSIS_FILE_NAME, source, self.analysis, ['id','topic','progress','bounce','playtime'])
    self.analysis = []

  def saveToFile(self, file_format, source, items, keys, type_name=""):
    if len(items) > 0:
      with open(file_format % (datetime.datetime.now().strftime('%s'), source), 'w') as f:
        writer = csv.writer(f)
        logging.info("Save %s items to file %s" % (len(items), f.name))
        for item in items:
          row = []
          if type_name != "":
            row.append(type_name)
          for key in keys:
            if key in item.keys():
              row.append(item[key])
              continue
            row.append('')
          writer.writerow(row)
        f.close()
