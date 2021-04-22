from pages import MailRu, MailList

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import MongoProcessing


chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

mailpage = MailRu()
maillist = MailList()
mongo = MongoProcessing()

driver.get(mailpage.url)
driver.find_element(mailpage.fLogin).send_keys(mailpage.login)
driver.find_element(mailpage.bEnterPassword).click()
driver.find_element(mailpage.fPassword).send_keys(mailpage.password)
driver.find_element(mailpage.bEnter).click()


counter = 0
mail_list = set()
size = len(mail_list)
while True:
    old_size = size
    mails = set(driver.find_element(maillist.aSingleMail()))
    mail_list = mail_list.union(mails)
    size = len(mail_list)
    if size == old_size:
        break
    actions = ActionChains(driver)
    actions.move_to_element(mail_list[-1])
    actions.perform()









