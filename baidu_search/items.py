# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BaiduSearchItem(scrapy.Item):
    index = scrapy.Field()
    web_url = scrapy.Field()
    url = scrapy.Field()
    img_name = scrapy.Field()
    save_path = scrapy.Field()
