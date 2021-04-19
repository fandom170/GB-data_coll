import MongoProcessing as mng
import page_processing
from page import PageMail
import requests



mail = PageMail()
mngl = mng.MongoProcessing()

pp = page_processing.NewspageProcessing(mail)

mail_dom = pp.get_page()
mail_news = pp.get_news_mail(mail_dom)


mngl.db_init('news')
mngl.collection_init("Mail")

counter = mngl.add_new_entries(mail_news)
print(f"{counter} new entries has been entered.")





