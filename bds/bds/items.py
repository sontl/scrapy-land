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
    code = scrapy.Field()
    created_date = scrapy.Field()
    price = scrapy.Field()
    square = scrapy.Field()
    title = scrapy.Field()
    project_url = scrapy.Field() # in full path
    url = scrapy.Field() # in full path
    
class Project(scrapy.Item):
    code = scrapy.Field()
    created_date = scrapy.Field()
    url = scrapy.Field() # in full path
    