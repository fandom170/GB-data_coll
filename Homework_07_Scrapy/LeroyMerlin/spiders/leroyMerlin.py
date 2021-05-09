import scrapy
from scrapy.http import HtmlResponse
from items import LeroymerlinItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroyMerlin'
    allowed_domains = ['leroymerlin.ru']
    
    def __init__(self, query):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']


    def parse(self, response: HtmlResponse):
        """"Take link """
        next_page = response.xpath(".//a[contains(@class,'s15wh9uj_plp')]/@href").extract()[-1]
        print("This is next page ", next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        
        item_links = response.xpath(".//div[contains(@class,'phytpj4_plp')]/a")
        
        # here can be processing of links
        
        for link in item_links:
            yield response.follow(link, callback=self.item_parse)

    def item_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_css('item_name', 'h1::text')
        loader.add_xpath('item_photos', ".//img[@alt='product image']/@src")
        loader.add_css('item_data_keys', "dt.def-list__term::text")
        loader.add_css('item_data_vals', "dd.def-list__definition::text")
        loader.add_xpath('item_price', ".//*[@class='primary-price']//span[@slot='price']/text()")
        loader.add_value('item_link', response.url)
        yield loader.load_item()

