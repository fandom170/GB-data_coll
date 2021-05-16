# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    linked_acc_id = scrapy.Field()
    linked_acc_name = scrapy.Field()
    data_type = scrapy.Field()
    full_name = scrapy.Field()
    profile_pic_url = scrapy.Field()
    user_data = scrapy.Field()

