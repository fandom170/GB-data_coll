# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookCollectItem(scrapy.Item):
    # define the fields for your item here like:

    book_name = scrapy.Field()
    book_link = scrapy.Field()
    authors = scrapy.Field()
    main_price = scrapy.Field()
    bargain_price = scrapy.Field()
    currency = scrapy.Field()
    book_rate = scrapy.Field()
