# -*- coding: utf-8 -*-
import scrapy


class FirstSpiderSpider(scrapy.Spider):
    name = 'first_spider'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
