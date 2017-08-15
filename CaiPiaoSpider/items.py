# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CaipiaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = scrapy.Field()
    red_one = scrapy.Field()
    red_two = scrapy.Field()
    red_three = scrapy.Field()
    red_four = scrapy.Field()
    red_five = scrapy.Field()
    red_six = scrapy.Field()
    blue = scrapy.Field()
    link = scrapy.Field()
    pass
