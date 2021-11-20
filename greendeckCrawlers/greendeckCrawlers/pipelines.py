# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo

class GreendeckcrawlersPipeline(object):
    #collection_name = 'flipkart'
    
    def __init__(self, mongo_uri, mongo_db,mongo_collection,mongo_username,mongo_password):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.mongo_username = mongo_username
        self.mongo_password = mongo_password
    

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection = crawler.settings.get('MONGODB_COLLECTION'),
            mongo_username = crawler.settings.get('MONGO_USERNAME'),
            mongo_password = crawler.settings.get('MONGO_PASSWORD')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri, username=self.mongo_username, password=self.mongo_password)
        self.db = self.client.get_database(self.mongo_db)
        self.collection_name = self.db.get_collection(self.mongo_collection)
        logging.debug("database:{}".format(self.db))
        logging.debug("collection:{}".format(self.collection_name))
        
    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each post
        #logging.debug(item['product_name'])
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        logging.debug("Post added to MongoDB")
        return item

    
