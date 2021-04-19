import requests
from datetime import datetime, date, timedelta
from lxml import html
import locale


class NewspageProcessing():
    # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    def __init__(self, page):
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                    '(KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
        self.name_xpath = page.name_xpath
        self.source_xpath = page.source_xpath
        self.link_xpath = page.link_xpath
        self.date_xpath = page.date_xpath
        self.page_url = page.url
        self.news_block = page.news_block
        self.news_date = page.news_date
        self.date_format = page.date_format
        self.page = page

    def get_page(self):
        response = requests.get(self.page_url, headers=self.header)
        dom = html.fromstring(response.text)
        return dom

    def get_news_lenta(self, dom):
        items = dom.xpath(self.news_block)
        news = []
        for elem in items:
            newsblock = {}
            news_link = self.page_url + elem.xpath(self.link_xpath)[0]
            news_name = elem.xpath(self.name_xpath)
            news_date = self.date_populating(elem, news_link)

            newsblock['name'] = self.news_name_handling(news_name)
            newsblock['link'] = news_link
            newsblock['date'] = news_date
            newsblock['source'] = elem.xpath(self.source_xpath)[0]
            news.append(newsblock)
        return news

    def get_news_yandex(self, dom):
        items = dom.xpath(self.news_block)
        news = []
        for elem in items:
            newsblock = {}
            news_link = self.page_url + elem.xpath(self.link_xpath)[0]
            news_name = elem.xpath(self.name_xpath)
            news_date = self.date_populating_yandex(elem)

            newsblock['name'] = self.news_name_handling(news_name)
            newsblock['link'] = news_link
            newsblock['date'] = news_date
            newsblock['source'] = elem.xpath(self.source_xpath)[0]
            news.append(newsblock)
        return news

    def get_news_mail(self, dom):
        items = dom.xpath(self.link_xpath)
        items_top = dom.xpath(self.page.top_link_xpath)
        items = items + items_top

        news = []
        for elem in items:
            newsblock = {}
            news_data = html.fromstring(requests.get(elem, headers=self.header).text)
            news_link = elem
            news_name = news_data.xpath(self.name_xpath)
            news_date = news_data.xpath(self.news_date)
            news_source = news_data.xpath(self.source_xpath)

            newsblock['name'] = news_name[0]
            newsblock['link'] = news_link
            newsblock['date'] = news_date[0]
            newsblock['source'] = news_source[0]
            news.append(newsblock)
            print(newsblock)
        return news


    def news_name_handling(self, news_name):

        if len(news_name) == 2:
            name = news_name[1]
        else:
            name = news_name[0]
        return name.strip().replace('\xa0', ' ')

    def date_populating(self, elem, news_link):
        news_date = elem.xpath(self.date_xpath)
        if len(news_date) == 1:
            date = news_date[0]
            date = date.strip()
        elif len(news_date) == 0:
            response = requests.get(news_link, headers=self.header)
            dom = html.fromstring(response.text)
            date = dom.xpath(self.news_date)[0]
        else:
            date = news_date[0]
        return date

    def date_formatting(self, date_line):
        date_line = date_line.capitalize()
        datetime_object = datetime.strptime(date_line, self.date_format)
        return datetime_object

    def date_populating_yandex(self, elem):
        news_date = elem.xpath(self.date_xpath)[0].split(' ')
        today = date.today()
        dateline = ''
        if len(news_date) == 1:
            d1 = today.strftime(self.date_format)
            dateline = news_date[0] + d1
        elif len(news_date) == 3 and news_date[0] == 'вчера':
            yesterday = today - timedelta(days=1)
            d1 = yesterday.strftime(self.date_format)
            dateline = news_date[0] + d1
        return dateline

