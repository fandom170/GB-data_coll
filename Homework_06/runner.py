from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Homework_06 import settings
from Homework_06.spiders import books24, labirint


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(books24.Books24Spider)
    process.crawl(labirint.LabirintSpider)


    process.start()




