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
    time.sleep(2)
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

"""email list len  23
Сегодня, 23:01
Сегодня, 21:48
Сегодня, 20:07
Сегодня, 20:06
Сегодня, 15:39
Сегодня, 15:37
Сегодня, 7:34
Вчера, 15:43
24 апреля, 16:10
23 апреля, 9:36
22 апреля, 20:19
22 апреля, 17:42
22 апреля, 17:41
22 апреля, 12:32
21 апреля, 3:15
20 апреля, 8:20
16 апреля, 15:03
15 апреля, 4:04
14 апреля, 11:03
13 апреля, 11:04
10 апреля, 8:24
9 апреля, 10:45
7 апреля, 18:35
First block completed
2 апреля, 15:14
new iteration
1 апреля, 13:33
new iteration
30 марта, 7:46
new iteration
29 марта, 19:41
new iteration
28 марта, 5:21
new iteration
27 марта, 13:42
new iteration
26 марта, 4:15
new iteration
25 марта, 14:40
new iteration
24 марта, 16:06
new iteration
24 марта, 16:04
new iteration
24 марта, 15:37
new iteration
24 марта, 10:35
new iteration
24 марта, 10:31
new iteration
24 марта, 10:25
new iteration
24 марта, 3:53
new iteration
23 марта, 21:52
new iteration
23 марта, 17:00
new iteration
22 марта, 16:34
new iteration
20 марта, 10:22
new iteration
19 марта, 17:39
new iteration
19 марта, 13:39
new iteration
19 марта, 8:00
new iteration
18 марта, 18:53
new iteration
18 марта, 15:34
new iteration
17 марта, 15:03
new iteration
11 марта, 16:53
new iteration
8 марта, 13:33
new iteration
4 марта, 18:26
new iteration
3 марта, 13:10
new iteration
3 марта, 0:01
new iteration
2 марта, 19:31
new iteration
1 марта, 3:01
new iteration
26 февраля, 11:55
new iteration
26 февраля, 11:12
new iteration
25 февраля, 21:32
new iteration
25 февраля, 20:46
new iteration
25 февраля, 9:01
new iteration
24 февраля, 10:42
new iteration
23 февраля, 13:28
new iteration
last email
full len 24
end of program execution. 62 new entries has been added."""



