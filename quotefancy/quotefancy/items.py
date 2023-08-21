# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotefancyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    quote = scrapy.Field(); author = scrapy.Field(); upvotes = scrapy.Field(); downvotes = scrapy.Field()
    image_urls = scrapy.Field();    images = scrapy.Field()

