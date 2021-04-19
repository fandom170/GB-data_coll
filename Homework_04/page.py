import requests


class PageLenta():
    def __init__(self):
        self.url = 'https://lenta.ru'
        self.name_xpath = ".//a//text()"
        self.link_xpath = ".//a/@href"
        self.date_xpath = ".//a/time/@datetime"
        self.news_block = "//div[@class='item']"
        self.source_xpath = "//head/title/text()"
        self.news_date = ".//div[@class='b-topic__info']/time/text()"
        self.date_format = '%H:%M, %B %b %Y'


class PageMail():
    def __init__(self):
        self.url = 'https://news.mail.ru/politics/'
        self.news_block = ".//div[@class='cols__inner']"
        self.date_format = '%H:%M, %d %B %Y'
        self.date_xpath = ""

        # First news
        self.top_link_xpath = ".//a[@class='newsitem__title link-holder']/@href"

        # Other news in the block
        self.link_xpath = ".//li[@class='list__item']//a/@href"

        # Inside news page
        self.source_xpath = ".//span[@class='note']/a/span/text()"
        self.news_date = ".//span[@class='note__text breadcrumbs__text js-ago']/@datetime"
        self.name_xpath = ".//h1[@class='hdr__inner']/text()"


class PageYandex():
    def __init__(self):
        self.url = 'https://yandex.ru/news'
        self.name_xpath = ".//a[@class='mg-card__link']/h2/text()"
        self.link_xpath = ".//a[@class='mg-card__link']/@href"
        self.date_xpath = ".//span[@class='mg-card-source__time']/text()"
        self.news_block = ".//article[contains(@class, 'mg-card')]"
        self.source_xpath = ".//a[@class='mg-card__source-link']/@aria-label"
        self.date_format = ', %d %B %Y'
