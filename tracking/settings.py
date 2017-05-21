# -*- coding: utf-8 -*-

# Scrapy settings for tracking project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
BUFFER_SIZE = 500000
FULL_SCAN_ENABLED = False
SCAN_GAP = 86400

IGNORE_DB = False

BOT_NAME = 'tracking'

MONGO_HOST = '172.16.0.120'
# MONGO_HOST = 'fetcher.zintow.com'
MONGO_PORT = 27017
MONGO_DB = 'Spider'
MONGO_COLLECTION = 'hots'
# MONGO_COLLECTION = 'hots_test'

DOUBAN_LATEST = 1000
DOUBAN_ALL_COMMENT_COUNT = 3
DOUBAN_REVIEW_COUNT = 200

PLAN_URL = "http://csr.zintow.com/tracking/plan?limit=200000000"
TRACKING_URL = "http://csr.zintow.com/tracking/tracker?limit=200000000"
FORBIDDEN_URL = "http://csr.zintow.com/tracking/forbidden?limit=200000000"
ENTITY_URL = "http://csr.zintow.com/entity/channel?limit=200000000"
ACCOUNT_URL = "http://csr.zintow.com"
TARGET_CHANNEL = "好好吃"

SPIDER_MODULES = ['tracking.spiders']
NEWSPIDER_MODULE = 'tracking.spiders'

DOWNLOADER_MIDDLEWARES = {
    "tracking.middleware.UserAgentMiddleware": 401,
    "tracking.middleware.CookiesMiddleware": 402,
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tracking (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = 'INFO'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 30

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 20
CONCURRENT_REQUESTS_PER_IP = 20

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tracking.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'tracking.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'tracking.pipelines.DefaultPipeline':200,
   'tracking.pipelines.FilePipeline':400,
   #'tracking.pipelines.DBPipeline':400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
