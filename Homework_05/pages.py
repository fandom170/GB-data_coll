from selenium.webdriver.common.by import By


class EmailInternal():
    def __init__(self):
        self.content = ".//div[@class='letter__body']"  #".//td[@class='main_border_mr_css_attr']"
        self.email_date = ".//div[@class='letter__date']"
        self.email_sender = ".//div[@class='letter__author']/span"

class MailRu ():
    def __init__(self):
        self.url = 'https://mail.ru'
        self.fLogin = ".//input[@name='login']"
        self.bEnterPassword = ".//button[@data-testid = 'enter-password']"
        self.fPassword = ".//input[@data-testid = 'password-input']"
        self.bEnter = ".//button[@data-testid='login-to-mail']"

        self.password = 'o%IyneXIrI11'
        self.login = 'study.ai_172@mail.ru'


class MailList ():
    def __init__(self):
        self.url = "https://e.mail.ru"
        self.singleMail = ".//a[contains(@class,'js-tooltip-direction_letter-bottom js-letter-list-item')]"




class MvideoMainPage():
    def __init__(self):
        self.url = "https://www.mvideo.ru"

        self.bNext = ".//div[contains(text(),'Новинки')]/ancestor::div[@class='section']//" \
                     "a[contains(@class, 'next-btn')]"
        self.item = ".//div[contains(text(),'Новинки')]/ancestor::div[@class='section']//li"
        self.item_data = ".//h4[@class='fl-product-tile-title fl-product-tile__title']/a"











