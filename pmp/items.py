# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class PmpItem(Item):
    createdAt = Field()
    imageUrl = Field()
    imageTitle = Field()
    pageUrl = Field()
    sourceId = Field()
    image_urls = Field()
    images = Field()
    filename = Field()
