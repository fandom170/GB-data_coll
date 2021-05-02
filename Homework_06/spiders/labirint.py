"""
1) Создать двух пауков по сбору данных о книгах с сайтов labirint.ru и book24.ru
2) Каждый паук должен собирать:
* Ссылку на книгу
* Наименование книги
* Автор(ы)
* Основную цену
* Цену со скидкой
* Рейтинг книги
3) Собранная информация дожна складываться в базу данных"""

import scrapy
from scrapy.http import HtmlResponse
from Homework_06.items import BookCollectItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/фантастика/?stype=0']

    def parse(self, response: HtmlResponse):
        book_links = response.xpath(".//a[@class='product-title-link']/@href").extract()
        next_page = response.css("div.pagination-number-viewport a.pagination-next__text::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for book in book_links:
            yield response.follow(book, callback=self.book_data)

    def book_data(self, response: HtmlResponse):
        book_name = response.css("h1::text").extract_first()
        book_link = response.url
        authors = response.css("div.authors a::text").extract()
        main_price = response.css("span.buying-priceold-val-number::text").extract_first()
        bargain_price = response.css("span.buying-pricenew-val-number::text").extract_first()
        currency = response.css("span.buying-pricenew-val-currency::text").extract_first()
        book_rate = response.css("div#rate::text").extract_first()
        yield BookCollectItem(book_name=book_name,
                              book_link=book_link,
                              authors=authors,
                              main_price=main_price,
                              bargain_price=bargain_price,
                              currency=currency,
                              book_rate=book_rate)
