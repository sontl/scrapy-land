# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BdsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Property(scrapy.Item):
    id = scrapy.Field()
    created_date = scrapy.Field()
    price = scrapy.Field()
    square = scrapy.Field()
    title = scrapy.Field()