from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException 
from .locators import BasePageLocators
import math

class BasePage:

    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        # окрыть браузер
        self.browser.get(self.url)
    
    def is_element_present(self, how, what):
        # если элемент есть на странице
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        # если элемент не появляется на странице в течение заданного времени
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

    def is_disappeared(self, how, what, timeout=4):
        # если элемент исчезает со страницы и через заданное время его уже нет
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException).\
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False

        return True

    def is_text_in_url(self, text):
        # если текс есть текущем url
        return text in self.browser.current_url

    def go_to_login_page(self):
        # Переход на страницу авторизации
        login_link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        login_link.click() 

    def should_be_login_link(self):
        # прверка наличия ссылки на авторизацию
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"

    def go_to_basket_page(self):
        # переход в корзину
        basket_link = self.browser.find_element(*BasePageLocators.BASKET_LINK)
        basket_link.click() 

    def should_be_authorized_user(self):
        # проверка, что пользователь авторизован
        assert self.is_element_present(*BasePageLocators.USER_ICON), "User icon is not presented," \
                                                                    " probably unauthorised user"        

    def solve_quiz_and_get_code(self): 
        # метод, для получения проверочного кода
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")        