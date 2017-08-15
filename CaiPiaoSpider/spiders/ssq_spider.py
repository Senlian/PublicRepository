#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
from CaiPiaoSpider.items import CaipiaospiderItem


class SsqSpider(scrapy.Spider):
    name = 'ssq'
    allowed_domains = ['kaijiang.500.com']
    start_urls = [r'http://kaijiang.500.com/ssq.shtml']

    def parse(self, response):
        links = response.xpath(r'//div[@class="iSelectList"]/a')
        # print response.body
        for link in links:
            url = link.xpath(r'@href').extract()[0].decode('utf-8')
            # print '-'*200
            yield scrapy.Request(url=str(url), callback=self.parse_data)
            # break
        pass

    def parse_data(self, response):
        item = CaipiaospiderItem()
        try:
            item['uid'] = response.xpath(r'//font[@class="cfont2"]/strong/text()').extract()[0]
            item['red_one'] = response.xpath(r'//div[@class="ball_box01"]/ul/li[1]/text()').extract()[0]
            item['red_two'] = response.xpath(r'//div[@class="ball_box01"]/ul/li[2]/text()').extract()[0]
            item['red_three'] = response.xpath(r'//div[@class="ball_box01"]/ul/li[3]/text()').extract()[0]
            item['red_four'] = response.xpath(r'//div[@class="ball_box01"]/ul/li[4]/text()').extract()[0]
            item['red_five'] = response.xpath(r'//div[@class="ball_box01"]/ul/li[5]/text()').extract()[0]
            item['red_six'] = response.xpath(r'//div[@class="ball_box01"]/ul/li[6]/text()').extract()[0]
            item['blue'] = response.xpath(r'//div[@class="ball_box01"]/ul/li[7]/text()').extract()[0]
            item['link'] = response.url
            yield item
        except Exception as e:
            item['uid'] = None
            item['red_one'] = None
            item['red_two'] = None
            item['red_three'] = None
            item['red_four'] = None
            item['red_five'] = None
            item['red_six'] = None
            item['blue'] = None
            item['link'] = response.url
            print '=' * 200
            print response.url
            print e
            print '=' * 200



if __name__ == '__main__':
    pass
