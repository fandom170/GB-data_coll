from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram import settings
from instagram.spiders import instaUsers

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(instaUsers.InstausersSpider)

    process.start()

