from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import time

from pages import MailRu, MailList, EmailInternal
import MongoProcessing

# web driver configuring
mailpage = MailRu()
maillist = MailList()
mailInternal = EmailInternal()
mongo = MongoProcessing.MongoProcessing()

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

# main page login
driver.get(mailpage.url)
driver.find_element(By.XPATH, mailpage.fLogin).send_keys(mailpage.login)
driver.find_element(By.XPATH, mailpage.bEnterPassword).click()

try:
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, mailpage.fPassword)))
    password_field.send_keys(mailpage.password)
except Exception as e:
    print(e)

driver.find_element(By.XPATH, mailpage.bEnter).click()

try:
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, maillist.singleMail)))
except Exception as e:
    print(e)
# processing list of emails after login

emails = []
time.sleep(2)
email_list = driver.find_elements(By.XPATH, maillist.singleMail)
print("email list len ", len(email_list))

for email in email_list:
    email_attrs = {}
    email_date_title = driver.find_element_by_xpath(maillist.email_date).get_attribute('title')
    email_date_text = driver.find_element_by_xpath(maillist.email_date).text
    email_sender = driver.find_element_by_xpath(maillist.email_sender).get_attribute('title')
    email_id = email.get_attribute('data-id')
    email_attrs['email_date_title'] = email_date_title
    email_attrs['email_date_text'] = email_date_text
    email_attrs['email_sender'] = email_date_title

    main_window = driver.current_window_handle
    print(main_window)

    email.send_keys(Keys.CONTROL + Keys.RETURN)
    #chwd = driver.window_handles
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    try:
        sender = driver.find_element_by_xpath(mailInternal.email_sender).getText()
        email_attrs['sender'] = sender
        sender_email = driver.find_element_by_xpath(mailInternal.email_sender).get_attribute('title')
        email_attrs['sender_email'] = sender_email
        email_date = driver.find_element_by_xpath(mailInternal.date).text
        email_attrs['email_date'] = email_date
        email_text = driver.find_element_by_xpath(mailInternal.content).text
        email_attrs['email_content'] = email_text

    except AttributeError :
        print("email skipped")
        continue
    email['id'] = email_attrs

    #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.execute_script("arguments[0].scrollIntoView();", email)


actions = ActionChains(driver)
actions.move_to_element(email_list[-1])
actions.perform()
"""
# scroll to take all available emails in the list
while True:
    list_len = len(emails)
    email_list = driver.find_elements(By.XPATH, maillist.singleMail)
    print("email list len ", len(email_list))
    for email in email_list:
        email_attrs = {}
        email_date_title = driver.find_element_by_xpath(maillist.email_date).get_attribute('title')
        email_date_text = driver.find_element_by_xpath(maillist.email_date).text
        email_sender = driver.find_element_by_xpath(maillist.email_sender).get_attribute('title')
        email_id = email.get_attribute('data-id')
        email_attrs['email_date_title'] = email_date_title
        email_attrs['email_date_text'] = email_date_text
        email_attrs['email_sender'] = email_date_title

        main_window = driver.current_window_handle
        print(main_window)

        email.send_keys(Keys.CONTROL + Keys.RETURN)
        # chwd = driver.window_handles
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        try:
            sender = driver.find_element_by_xpath(mailInternal.email_sender).getText()
            email_attrs['sender'] = sender
            sender_email = driver.find_element_by_xpath(mailInternal.email_sender).get_attribute('title')
            email_attrs['sender_email'] = sender_email
            email_date = driver.find_element_by_xpath(mailInternal.date).text
            email_attrs['email_date'] = email_date
            email_text = driver.find_element_by_xpath(mailInternal.content).text
            email_attrs['email_content'] = email_text

        except AttributeError:
            print("email skipped")
            continue

        email['id'] = email_attrs

        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.execute_script("arguments[0].scrollIntoView();", email)

        new_list_len = len(emails)

    if list_len == new_list_len:
        print("last email")
        break

print("full len", len(email_list))

email_data = []

for email in email_list:
    print("Loping inside emails")
    email_page = {}
    id = email.get_attribute('data-uidl-id')
    mail_url = email.get_attribute('href')
    url = maillist.url + mail_url
    driver.get(url)

    sender = driver.find_element_by_xpath(mailInternal.sender).getText()
    sender_email = driver.find_element_by_xpath(mailInternal.sender).get_attribute('title')
    email_text = driver.find_element_by_xpath(mailInternal.content).text
    email_date = driver.find_element_by_xpath(mailInternal.date).text

    driver.back()

    email_page['_id'] = id
    email_page['from'] = sender
    email_page['from_email'] = sender_email
    email_page['date'] = email_date
    email_page['mail_text'] = email_text

    print(email_page)
"""
driver.close()

mongo.db_init("homework_05")
mongo.collection_init("Mailru")
counter = mongo.add_new_entries_mail(emails)

print(f"end of program execution. {counter} new entries has been added.")



