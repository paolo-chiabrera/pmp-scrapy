# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem
from datetime import datetime
from ntpath import basename


class BeforeImagePipeline(object):
    def process_item(self, item, spider):
        item['image_urls'] = [item['imageUrl']]

        return item


class AfterImagePipeline(object):
    def open_spider(self, spider):
        self.startDatetime = datetime.now()

    def process_item(self, item, spider):
        item['createdAt'] = self.startDatetime
        item['sourceId'] = spider.name
        item['filename'] = basename(item['images'][0]['path'])

        del item['image_urls']
        del item['images']

        return item


class MongoPipeline(object):
    collection_name = 'images'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.startDatetime = datetime.now()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print(item)

        try:
            self.db[self.collection_name].insert_one(dict(item))
        except pymongo.errors.DuplicateKeyError:
            raise DropItem(f'DuplicateKeyError: {item["imageUrl"]}')
        except:
            raise DropItem(f'Something went wrong: {item["imageUrl"]}')

        return item
