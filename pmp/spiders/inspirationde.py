# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pmp.items import PmpItem


class InspirationdeSpider(CrawlSpider):
    name = 'inspirationde'
    allowed_domains = ['inspirationde.com']
    start_urls = ['https://www.inspirationde.com/']

    count = 1
    offset = 1
    totalImages = 0

    def parse_image(self, response):
        item = PmpItem()
        item['pageUrl'] = response.url
        item['imageTitle'] = response.css(
            '#post-featured-photo img.featured-thumb::attr(alt)').extract_first()
        item['imageUrl'] = response.css(
            '#post-featured-photo img.featured-thumb::attr(src)').extract_first()

        yield item

    def parse(self, response):
        imagePages = set(response.css('#masonry a.thumb-holder::attr(href)'))

        if len(imagePages) > 0:
            # follow links to image pages
            for href in imagePages:
                yield response.follow(href, self.parse_image)

            self.totalImages += len(imagePages)

            self.logger.info(
                f'page: {self.count}, totalImages: {self.totalImages}, url: {response.url}')

            self.count += 1
            offset = self.count * self.offset
            nextPageUrl = f'https://www.inspirationde.com/page/{offset}'

            # follow pagination links
            yield response.follow(nextPageUrl, self.parse)
