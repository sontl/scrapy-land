# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import boto3
from scrapy.conf import settings
from bds.items import Property
from bds.items import Project

class BdsPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    
    property_collection_name = "properties"
    project_collection_name = "projects"
    
    def __init__(self, mongo_url, mongo_db, mongo_port, mongo_user, mongo_password):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password
        #self.mongo_collection = mongo_collection
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls (
            mongo_url = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DATABASE'),
            mongo_port = crawler.settings.get('MONGO_PORT'),
            mongo_user = crawler.settings.get('MONGO_USER'),
            mongo_password = crawler.settings.get('MONGO_PASSWORD'),
            #mongo_collection = crawler.settings.get('MONGO_COLLECTION')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.db.authenticate(self.mongo_user, self.mongo_password)
        
    def close_spider(self, spider):
        self.client.close()
    def process_item(self, item, spider):
        if isinstance(item, Property):
            properties_coll = self.db[self.property_collection_name]
            existing_record = properties_coll.find_one({
                "origin_id": item.get("origin_id"),
                "url" : item.get("url")
            })
            if existing_record is None:
                print("-" * 40);
                print("new record. Inserting to database");
                print("-" * 40);
                properties_coll.insert(dict(item))
            else:
                print("Record is existing in database");
        elif isinstance(item, Project):
            projects_coll = self.db[self.project_collection_name]
            projects_coll.insert(dict(item))
        else:
            self.db[self.property_collection_name].insert(dict(item))
        return item

class DynamoPipeline(object):

    def __init__(self, dynamo_url, dynamo_db, dynamo_port):
        self.dynamo_url = dynamo_url
        self.dynamo_db = dynamo_db
        self.dynamo_port = dynamo_port
        #self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls (
            dynamo_url = crawler.settings.get('MONGO_URL', 'ds047198.mlab.com'),
            dynamo_db = crawler.settings.get('MONGO_DATABASE', 'sontl'),
            dynamo_port = crawler.settings.get('MONGO_PORT', 47198),
            #mongo_collection = crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('users')
        
    def close_spider(self, spider):
        #do nothing
        print("spider closed, dynamodb do nothing");

    def process_item(self, item, spider):
        self.table.put_item(
            Item={
                    'username': 'janedoe',
                    'first_name': 'Jane',
                    'last_name':  item.get("origin_id"),
                    'age': 25,
                    'account_type': item.get("url"),
                }
            )
        return item