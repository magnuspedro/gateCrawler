# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazoncrawlerItem(scrapy.Item):
    code = scrapy.Field()
    product = scrapy.Field()
    price = scrapy.Field()
    shipping = scrapy.Field()
    small_price = scrapy.Field()
    link = scrapy.Field()

class AmericanasItem(scrapy.Item):
    code = scrapy.Field()
    product = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()

