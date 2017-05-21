# -*- coding: utf-8 -*-
import csv
import datetime
import logging
import codecs
import pymongo
import re
import json
from tracking.items import PlaycountItem, DurationItem
from tracking.items import PageviewItem, CommentsCountItem, TopicItem
from pipelines import FilePipeline

def log(ut, suffix):
  logging.info(('Update ' if ut == 1 else 'Insert ') + suffix)

PLAYCOUNT_FILE_NAME = 'playcount.%s.%s.json'
DURATION_FILE_NAME = 'duration.%s.%s.json'
PAGEVIEW_FILE_NAME = 'pageview.%s.%s.json'
COMMENTSCOUNT_FILE_NAME = 'commentscount.%s.%s.json'
TOPIC_FILE_NAME = 'topic.%s.%s.json'
RECOMMENDATION_FILE_NAME = 'recommendation.%s.%s.json'
REPOST_FILE_NAME = 'repost.%s.%s.json'
UP_FILE_NAME = 'up.%s.%s.json'
DOWN_FILE_NAME = 'down.%s.%s.json'
COLLECTION_FILE_NAME = 'collection.%s.%s.json'
CHANNEL_FILE_NAME = 'channel.%s.%s.json'
RANKING_FILE_NAME = 'ranking.%s.%s.json'
BIGV_FILE_NAME = 'bigv.%s.%s.json'

class JsonPipeline(FilePipeline):

  def __init__(self):
    FilePipeline.__init__(self)

  def savePlaycountToFile(self, source):
    self.saveToJsonFile(PLAYCOUNT_FILE_NAME, source, self.playcount, type_name="playcount")
    self.playcount = []

  def saveDurationToFile(self, source):
    self.saveToJsonFile(DURATION_FILE_NAME, source, self.duration, type_name="duration")
    self.duration = []

  def savePageviewToFile(self, source):
    self.saveToJsonFile(PAGEVIEW_FILE_NAME, source, self.pageview, type_name="pageview")
    self.pageview = []

  def saveCommentsCountToFile(self, source):
    self.saveToJsonFile(COMMENTSCOUNT_FILE_NAME, source, self.commentscount, type_name="commentscount")
    self.commentscount = []

  def saveTopicToFile(self, source):
    self.saveToJsonFile(TOPIC_FILE_NAME, source, self.topic, type_name="topic")
    self.topic = []

  def saveRecommendationToFile(self, source):
    self.saveToJsonFile(RECOMMENDATION_FILE_NAME, source, self.recommendation, type_name="recommendation")
    self.recommendation = []

  def saveRepostToFile(self, source):
    self.saveToJsonFile(REPOST_FILE_NAME, source, self.repost, type_name="repost")
    self.repost = []

  def saveUpToFile(self, source):
    self.saveToJsonFile(UP_FILE_NAME, source, self.up, type_name="up")
    self.up = []

  def saveDownToFile(self, source):
    self.saveToJsonFile(DOWN_FILE_NAME, source, self.down, type_name="down")
    self.down = []

  def saveCollectionToFile(self, source):
    self.saveToJsonFile(COLLECTION_FILE_NAME, source, self.collection, type_name="collection")
    self.collection = []

  def saveChannelToFile(self, source):
    self.saveToJsonFile(CHANNEL_FILE_NAME, source, self.channel, type_name="channel")
    self.channel = []

  def saveRankingToFile(self, source):
    self.saveToJsonFile(RANKING_FILE_NAME, source, self.ranking, type_name="ranking")
    self.ranking = []

  def saveBigVToFile(self, source):
    self.saveToJsonFile(BIGV_FILE_NAME, source, self.bigv, type_name="bigv")
    self.bigv = []

  def saveToJsonFile(self, file_format, source, items, type_name=""):
    if len(items) > 0:
      with open(file_format % (datetime.datetime.now().strftime('%s'), source), 'w') as f:
        logging.info("Save %s items to file %s" % (len(items), f.name))
        for item in items:
          js_str = json.dumps(dict(item), ensure_ascii=False)
          js = json.loads(js_str)
          js["types"] = type_name
          js_result = json.dumps(dict(js), ensure_ascii=False) + str("\n")
          f.write(js_result)
        f.close()
