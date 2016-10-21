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
    origin_id = scrapy.Field() # id created by the owner website
    code = scrapy.Field()
    created_date = scrapy.Field() # the date that this product is posted
    expiry_date = scrapy.Field()
    price = scrapy.Field()
    square = scrapy.Field()
    title = scrapy.Field()
    project_url = scrapy.Field() # url of the similar products
    url = scrapy.Field() # url of the crawled page in full path
    address = scrapy.Field()
    post_type = scrapy.Field()
    contact_info = scrapy.Field()
    content = scrapy.Field()
    extra_content = scrapy.Field()
    
    
class Project(scrapy.Item):
    origin_id = scrapy.Field() # id created by the owner website
    code = scrapy.Field()
    created_date = scrapy.Field()
    url = scrapy.Field() # in full path
    name = scrapy.Field()
    other_name = scrapy.Field()
    
    