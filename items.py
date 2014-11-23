# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WaterfallItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    classification_type = scrapy.Field()
    height = scrapy.Field()
    width = scrapy.Field()
    ownership = scrapy.Field() # (public/priate)
    accessibility = scrapy.Field() #("yes" or "inaccessible without permission from owner")
