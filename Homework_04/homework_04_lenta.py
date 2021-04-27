import MongoProcessing as mng
import page_processing
from page import PageLenta
import requests



lenta = PageLenta()
mngl = mng.MongoProcessing()

pp = page_processing.NewspageProcessing(lenta)

lenta_dom = pp.get_page()
lenta_news = pp.get_news_lenta(lenta_dom)

print(len(lenta_news))

mngl.db_init('news')
mngl.collection_init("Lenta")

counter = mngl.add_new_entries(lenta_news)
print(f"{counter} new entries have been entered.")





