import MongoProcessing as mng
import page_processing
from page import PageYandex
import requests



yandex = PageYandex()
mngl = mng.MongoProcessing()

pp = page_processing.NewspageProcessing(yandex)

yandex_dom = pp.get_page()
yandex_news = pp.get_news_yandex(yandex_dom)

print(len(yandex_news))

mngl.db_init('news')
mngl.collection_init("Yandex")

counter = mngl.add_new_entries(yandex_news)
print(f"{counter} new entries has been entered.")





