# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    builds_on = scrapy.Field()
    institute = scrapy.Field()


class FacultyItem(scrapy.Item):
    name = scrapy.Field()
    institutes = scrapy.Field()
