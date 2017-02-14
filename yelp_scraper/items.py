# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Restaurant(scrapy.Item):
    cuisine = scrapy.Field()
    name = scrapy.Field()
    neighborhood = scrapy.Field()
    stars = scrapy.Field()
    numberOfReviews = scrapy.Field()
    url = scrapy.Field()
    ID = scrapy.Field()
    address = scrapy.Field()
    author = scrapy.Field()
    review_stars = scrapy.Field()
    review_body = scrapy.Field()
    review_date = scrapy.Field()
    price = scrapy.Field()

