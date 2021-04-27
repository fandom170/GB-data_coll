import json

from pages import MvideoMainPage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import MongoProcessing
import time

from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('start-maximized')

mvideo = MvideoMainPage()
mongo = MongoProcessing.MongoProcessing()

driver = webdriver.Chrome(options=chrome_options)

driver.get(mvideo.url)

items = []


products = driver.find_elements_by_xpath(mvideo.item)
product_len = len(products)
actions = ActionChains(driver)
actions.move_to_element(products[0]).perform()
button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, mvideo.bNext))
        )
while True:
    time.sleep(1)
    button.click()
    time.sleep(1)
    old_len = len(products)
    new_products = driver.find_elements_by_xpath(mvideo.item)
    products = list(dict.fromkeys(products + new_products))
    new_len = len(products)
    if old_len == new_len:
        break


new_products = []
for product in products:
    new_item = {}
    item_data = product.find_element_by_xpath(mvideo.item_data).get_attribute('data-product-info')
    item_dict = json.loads(item_data)
    new_item['Name'] = item_dict['productName']
    new_item['Category'] = item_dict['productCategoryName']
    new_item['VendorName'] = item_dict['productVendorName']
    new_item['Price'] = item_dict['productPriceLocal']
    new_products.append(new_item)

mongo.db_init("homework_05")
mongo.collection_init("mvideo")
mongo.add_new_entries_mvideo(new_products)


driver.close()





