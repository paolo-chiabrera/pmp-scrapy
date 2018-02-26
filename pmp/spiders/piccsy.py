# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pmp.items import PmpItem


class PiccsySpider(CrawlSpider):
    name = 'piccsy'
    allowed_domains = ['piccsy.com']
    start_urls = ['http://piccsy.com/']

    count = 0
    offset = 20
    totalImages = 0

    def parse_image(self, response):
        item = PmpItem()
        item['pageUrl'] = response.url
        item['imageTitle'] = response.css(
            '.p-picc img.ctx-post-left-image::attr(alt)').extract_first()
        item['imageUrl'] = response.css(
            '.p-picc img.ctx-post-left-image::attr(src)').extract_first()

        yield item

    def parse(self, response):
        imagePages = set(response.css('div.p-picc > a::attr(href)'))

        if len(imagePages) > 0:
            # follow links to image pages
            for href in imagePages:
                yield response.follow(href, self.parse_image)

            self.totalImages += len(imagePages)

            self.logger.info(
                f'page: {self.count}, totalImages: {self.totalImages}, url: {response.url}')

            self.count += 1
            offset = self.count * self.offset
            nextPageUrl = f'http://piccsy.com/?offset={offset}'

            # follow pagination links
            yield response.follow(nextPageUrl, self.parse)
