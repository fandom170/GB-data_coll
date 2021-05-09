from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from spiders.leroyMerlin import LeroymerlinSpider
from LeroyMerlin import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    query = input('Please enter desired item for data collection:\n')

    if not query:
        query = 'обои'

    process.crawl(LeroymerlinSpider, query=query)
    process.start()
