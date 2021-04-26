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

emails = {}
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

    chwd = driver.window_handles
    print(chwd)
    print(len(chwd))

    driver.switch_to.window(driver.window_handles[-1])
    #for w in chwd:
    #    if (w != main_window):
    #        #driver.switch_to.window(w)
     #       driver.switch_to.window(driver.window_handles[-1])
     #       print("w", w)
    #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    #driver.switch_to.window(main_window)
    # do something
    time.sleep(2)
    print("window handling")
    #sender = driver.find_element_by_xpath(mailInternal.sender).getText()
    #sender_email = driver.find_element_by_xpath(mailInternal.sender).get_attribute('title')
    #email_text = driver.find_element_by_xpath(mailInternal.content).text
    #email_date = driver.find_element_by_xpath(mailInternal.date).text
    #driver.close()

    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    #driver.switch_to.window(main_window)
    driver.switch_to.window(driver.window_handles[0])

    #email_attrs['email_content'] = email_content
    # Switch back to the first tab with URL A
#    driver.back()
    driver.execute_script("arguments[0].scrollIntoView();", email)


actions = ActionChains(driver)
actions.move_to_element(email_list[-1])
actions.perform()
"""
# scroll to take all available emails in the list
while True:
    old_len = len(email_list)
    new_emails = driver.find_elements_by_xpath(maillist.singleMail)
    last_email = email_list[-1]
    for email in new_emails:
        email_list.append(email)
    new_last_email = email_list[-1]
    new_len = len(email_list)
    time.sleep(3)
    driver.execute_script("arguments[0].scrollIntoView();", email_list[-1])

    if last_email == new_last_email:
        print("last email")
        break

print("full len", len(email_list))

#removing of duplicates for email.list
email_list = list(dict.fromkeys(email_list))

email_data = []

for email in email_list:
    print("Loping inside emails")
    email_page = {}
    id = email.get_attribute('data-uidl-id')
    mail_url = email.get_attribute('href')
    url = maillist.url + mail_url
    driver.get(url)

    sender = driver.find_element_by_xpath(emailInternal.sender).getText()
    sender_email = driver.find_element_by_xpath(emailInternal.sender).get_attribute('title')
    email_text = driver.find_element_by_xpath(emailInternal.content).text
    email_date = driver.find_element_by_xpath(emailInternal.date).text

    driver.back()

    email_page['_id'] = id
    email_page['from'] = sender
    email_page['from_email'] = sender_email
    email_page['date'] = email_date
    email_page['mail_text'] = email_text

    print(email_page)
"""
driver.close()

"""mongo.db_init("homework_05")
mongo.collection_init("Mailru")
mongo.add_new_entries_mail(email_data)"""

print("end of program execution")



