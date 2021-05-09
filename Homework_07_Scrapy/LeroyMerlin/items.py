# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def remove_gaps(dataLine):
    convertedDataLine = dataLine \
        .replace('\n', '')\
        .strip()

    return convertedDataLine

class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_name = scrapy.Field(output_processor=TakeFirst())
    item_photos = scrapy.Field()
    item_data_keys = scrapy.Field(input_processor=MapCompose(remove_gaps))
    item_data_vals = scrapy.Field(input_processor=MapCompose(remove_gaps))
    item_price = scrapy.Field(output_processor=TakeFirst())
    item_link = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
