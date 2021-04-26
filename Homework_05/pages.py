from selenium.webdriver.common.by import By


class MailRu ():
    def __init__(self):
        self.url = 'https://mail.ru'
        self.fLogin = ".//input[@name='login']"
        self.bEnterPassword = ".//button[@data-testid = 'enter-password']"
        self.fPassword = ".//input[@data-testid = 'password-input']"
        self.bEnter = ".//button[@data-testid='login-to-mail']"

        self.password = 'NextPassword172'
        self.login = 'study.ai_172@mail.ru'

class MailList ():
    def __init__(self):
        self.url = "https://e.mail.ru"
        self.singleMail = ".//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal']"
        self.email_date = ".//div[@class='llc__item llc__item_date']"
        self.email_sender = ".//span[@class='ll-crpt']"



class EmailInternal():
    def __int__(self):
        self.content = ".//td[@class='main_border_mr_css_attr']"
        self.date = ".//div[@class='letter__date']"
        self.sender = ".//div[@class='letter__author']/span[@class = 'letter-contact']"


class MvideoMainPage():
    def __init__(self):
        self.url = "https://www.mvideo.ru"

        self.bNext = ".//div[contains(text(),'Новинки')]/ancestor::div[@class='section']//" \
                     "a[contains(@class, 'next-btn')]"
        self.item = ".//div[contains(text(),'Новинки')]/ancestor::div[@class='section']//li"
        self.item_data = ".//h4[@class='fl-product-tile-title fl-product-tile__title']/a"











