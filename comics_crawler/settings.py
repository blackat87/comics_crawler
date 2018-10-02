# -*- coding: utf-8 -*-

# Scrapy settings for comics_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'comics_crawler'

SPIDER_MODULES = ['comics_crawler.spiders']
NEWSPIDER_MODULE = 'comics_crawler.spiders'

#Enabled RetryMiddleware
RETRY_ENABLED = True
RETRY_TIMES = 2
RETRY_HTTP_CODES = [500, 502, 503, 504]

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'comics_crawler.middlewares.ComicsCrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'comics_crawler.middlewares.ComicsCrawlerDownloaderMiddleware': 543,
    'comics_crawler.middlewares.RandomProxyIpMiddleware': 1,
    'comics_crawler.middlewares.RandomUserAgentMiddleware': 2,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#extension for automatically throttling crawling speed based on load of both the Scrapy server and the website you are crawling
#automatically adjust scrapy to the optimum crawling speed, so the user doesn’t have to tune the download delays 
#to find the optimum one.
#The user only needs to specify the maximum concurrent requests it allows, and the extension does the rest
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

HTTPERROR_ALLOWED_CODES = [404,403]

#Configure FEED settings for data export
import os

full_path = os.path.realpath(__file__)
dirpath = os.path.dirname(full_path)

FEED_URI = 'file://%s/results/export_comicsbox.csv' % dirpath
FEED_FORMAT = 'csv'
FEED_EXPORT_ENCODING = 'utf-8'
FEED_EXPORT_FIELDS = ['editor', 'series', 'date', 'pages', 'title', 'arts', 'scripts', 'inks', 'colors']

LOG_FILE = 'comicsbox_log.txt'
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'