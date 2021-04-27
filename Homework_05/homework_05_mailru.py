from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import time

import pages
import MongoProcessing

# web driver configuring
mailPage = pages.MailRu()
mailList = pages.MailList()
mailInternal = pages.EmailInternal()
mongo = MongoProcessing.MongoProcessing()

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

# main page login
driver.get(mailPage.url)
driver.find_element(By.XPATH, mailPage.fLogin).send_keys(mailPage.login)
driver.find_element(By.XPATH, mailPage.bEnterPassword).click()

try:
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, mailPage.fPassword)))
    password_field.send_keys(mailPage.password)
except Exception as e:
    print(e)

driver.find_element(By.XPATH, mailPage.bEnter).click()

try:
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, mailList.singleMail)))
except Exception as e:
    print(e)
# processing list of emails after login

emails = []
email_ids = []
time.sleep(2)
email_list = driver.find_elements(By.XPATH, mailList.singleMail)
print("email list len ", len(email_list))
main_window = driver.current_window_handle

for email in email_list:
    email_attrs = {}
    email_id = email.get_attribute('data-id')

    email.send_keys(Keys.CONTROL + Keys.RETURN)
    driver.switch_to.window(driver.window_handles[-1])
    ################################################################
    time.sleep(5)
    email_date = WebDriverWait(driver, 10)\
        .until(EC.presence_of_element_located((By.XPATH, mailInternal.email_date))).text
    email_attrs['email_date'] = email_date
    print(email_date)
    sender = driver.find_element_by_xpath(mailInternal.email_sender).text
    email_attrs['sender'] = sender
    sender_email = driver.find_element_by_xpath(mailInternal.email_sender).get_attribute('title')
    email_attrs['sender_email'] = sender_email
    email_text = driver.find_element_by_xpath(mailInternal.content).text
    email_attrs['email_content'] = email_text
    emails.append(email_attrs)
    email_ids.append(email_id)

    driver.close()
    driver.switch_to.window(main_window)
    driver.execute_script("arguments[0].scrollIntoView();", email)

print("First block completed")
# scroll to take all available emails in the list
while True:
    email_list = driver.find_elements(By.XPATH, mailList.singleMail)
    list_len = len(emails)
    for email in email_list:
        email_id = email.get_attribute('data-id')
        if email_id in email_ids:
            continue
        email_attrs = {}
        email_ids.append(email_id)

        email.send_keys(Keys.CONTROL + Keys.RETURN)
        driver.switch_to.window(driver.window_handles[-1])
        ################################################################
        time.sleep(5)
        email_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, mailInternal.email_date))
        ).text
        email_attrs['email_date'] = email_date
        print(email_date)
        sender = driver.find_element_by_xpath(mailInternal.email_sender).text
        email_attrs['sender'] = sender
        sender_email = driver.find_element_by_xpath(mailInternal.email_sender).get_attribute('title')
        email_attrs['sender_email'] = sender_email
        email_text = driver.find_element_by_xpath(mailInternal.content).text
        email_attrs['email_content'] = email_text
        emails.append(email_attrs)

        driver.close()
        driver.switch_to.window(main_window)

        driver.execute_script("arguments[0].scrollIntoView();", email)

        print("new iteration")

    new_list_len = len(emails)
    if list_len == new_list_len:
        print("last email")
        break

print("full len", len(email_list))

driver.close()

mongo.db_init("homework_05")
mongo.collection_init("Mailru")
counter = mongo.add_new_entries_mail(emails)

print(f"end of program execution. {counter} new entries has been added.")



