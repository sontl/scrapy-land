import scrapy

class Property(scrapy.Item):
    id = scrapy.Field()
    created_date = scrapy.Field()
    price = scrapy.Field()
    square = scrapy.Field()
    title = scrapy.Field()