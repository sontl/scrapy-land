import pymongo

class MongoPipeline(object):
    
    collection_name = "scrapy_items"
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_url = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls {
            mongo_uri = crawler.settings.get('MONGO_URI', 'ds047198.mlab.com:47198'),
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'sontl')
        }
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        
    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item