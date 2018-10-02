# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    series = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    editor = scrapy.Field()
    pages = scrapy.Field()
    scripts = scrapy.Field()
    arts = scrapy.Field()
    inks = scrapy.Field()
    colors = scrapy.Field()