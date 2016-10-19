# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from bds.items import Property
from bds.items import Project

class BdsPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    
    property_collection_name = "properties"
    project_collection_name = "projects"
    
    def __init__(self, mongo_url, mongo_db, mongo_port):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port
        #self.mongo_collection = mongo_collection
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls (
            mongo_url = crawler.settings.get('MONGO_URL', 'ds047198.mlab.com'),
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'sontl'),
            mongo_port = crawler.settings.get('MONGO_PORT', 47198),
            #mongo_collection = crawler.settings.get('MONGO_COLLECTION')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.db.authenticate("test", "test")
        
    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        if isinstance(item, Property):
            self.db[self.property_collection_name].insert(dict(item))
        elif isinstance(item, Project):
            self.db[self.project_collection_name].insert(dict(item))
        else: 
            self.db[self.property_collection_name].insert(dict(item))
        return item