# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    job_title = scrapy.Field()
    ent_name = scrapy.Field()
    ent_link = scrapy.Field()
    compensation = scrapy.Field()
    location = scrapy.Field()
    time = scrapy.Field()
    requirements = scrapy.Field()
    jd = scrapy.Field()
    more_info = scrapy.Field()
