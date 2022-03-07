# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    #name = scrapy.Field()
    nickname = scrapy.Field()
    print(nickname)
    content = scrapy.Field()
    print(content)
    time = scrapy.Field()
    score = scrapy.Field()