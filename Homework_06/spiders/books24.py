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


class Books24Spider(scrapy.Spider):
    name = 'books24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/tayny-sensatsii-fakty-katastrofy-1442/']

    counter = 2

    def parse(self, response: HtmlResponse):
        book_links = response.xpath(".//a[contains(@class, 'product-card__name')]//@href").extract()
        nothing = response.xpath(".//div[@class='catalog__product-list-holder']/div/text()").extract_first
        if 'Извините, ничего не найдено' not in str(nothing):
            next_page = f"https://book24.ru/catalog/tayny-sensatsii-fakty-katastrofy-1442/page-{self.counter}/"
        else:
            next_page = None
        self.counter += 1
        if next_page:
            print(next_page)
            yield response.follow(next_page, callback=self.parse)
        for book in book_links:
            yield response.follow(book, callback=self.book_data)

    def book_data(self, response: HtmlResponse):
        book_name = response.css("h1.item-detail__title::text").extract_first()
        book_link = response.url
        authors = response.xpath(".//span[contains(text(), 'Автор')]/following-sibling::span/a/text() | "
                                 ".//span[contains(text(), 'Переводчики')]/following-sibling::span/text()") .extract()
        main_price = response.css("div.item-actions__price-old::text").extract_first()
        bargain_price = response.css("div.item-actions__price b::text").extract_first()
        currency = response.css("div.item-actions__price::text").extract_first()
        book_rate = response.css("div.rating__rate-value._bold::text").extract_first()
        yield BookCollectItem(book_name=book_name,
                              book_link=book_link,
                              authors=authors,
                              main_price=main_price,
                              bargain_price=bargain_price,
                              currency=currency,
                              book_rate=book_rate)
