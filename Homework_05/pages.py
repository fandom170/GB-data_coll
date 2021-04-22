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



    def fLogin(self):
        return By.XPATH(self.fLogin)

    def bEnterPassword(self):
        return By.XPATH(self.bEnterPassword)

    def fPassword(self):
        return By.XPATH(self.fPassword)

    def bEnter(self):
        return By.XPATH(self.bEnter)


class MailList ():
    def __init__(self):
        self.singleMail = ".//a[contains(@class, 'js-letter-list-item llc_normal')]"

    def aSingleMail(self):
        return By.XPATH(self.singleMail)



class emailInternal():
    pass


class MvideoMainPage():
    def __init__(self):
        self.url = "https://www.mvideo.ru"

        self.bNext = ".//div[contains(text(),'Новинки')]/ancestor::div[@class='section']//" \
                     "a[contains(@class, 'next-btn')]"
        self.item = ".//div[contains(text(),'Новинки')]/ancestor::div[@class='section']//li"
        self.item_data = ".//h4[@class='fl-product-tile-title fl-product-tile__title']/a"











