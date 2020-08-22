# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpdetailsItem(scrapy.Item):
    Name = scrapy.Field()
    website_name = scrapy.Field()
    website_link = scrapy.Field()
    phone = scrapy.Field()
    Direction = scrapy.Field()
    category = scrapy.Field()
    find = scrapy.Field()
    near = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    competitor1 = scrapy.Field()
    competitor2 = scrapy.Field()
    competitor3 = scrapy.Field()
    competitor4 = scrapy.Field()





