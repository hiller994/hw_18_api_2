import time

import allure
from selene import browser, have
import requests


LOGIN = "Test-po4ta@bk.ru"
PASSWORD = "Qwerty123@"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"

#Тест UI
def test_login():
    """Successful authorization to some demowebshop (UI)"""
    with allure.step("Open login page"):
        browser.open("http://demowebshop.tricentis.com/login")

    with allure.step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with allure.step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))

#Тест API + UI
def test_login_though_api():
    """Successful authorization to some demowebshop (API)"""
    with allure.step("Login with api"):
        '''
        #ЗАКОММЕНТИЛИ РУЧНОЙ ШАГ АВТОРИЗАЦИИ
        #with allure.step("Open login page"):
        #    browser.open("http://demowebshop.tricentis.com/login")
        #
        #with allure.step("Fill login form"):
        #    browser.element("#Email").send_keys(LOGIN)
        #    browser.element("#Password").send_keys(PASSWORD).press_enter()
        '''

        resoult = requests.post(url=API_URL + '/login',
                                data= {"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
                                allow_redirects=False) #ВЫРУБАЕИ РЕДИРЕКТ, ЧТОБЫ ЗАПРОС АВТОРИЗАЦИИ НЕ СРЕДИРЕКТИЛ, А ОСТАЛСЯ С КОДОМ 302
        print(resoult.status_code)
        print(resoult.text)
        print(resoult.cookies)
        #ПОСЛЕ ТОГО, КАК СОВЕРШИЛИ АВТОРИЗАЦИЮ И ПОЛУЧИЛИ 302, ИЗ КУКОВ НУЖНО ДОСТАТЬ ТОКЕН

    with allure.step("Get cookie from API"):
        cookie = resoult.cookies.get("NOPCOMMERCE.AUTH") # в куках NOPCOMMERCE.AUTH=7AFEBDE9DB1F20...

    with allure.step("Set cookie from API"):
        browser.open(WEB_URL) #Открываем нашу страницу
        browser.driver.add_cookie({"name":"NOPCOMMERCE.AUTH", "value": cookie}) #и передаем наш токен для этого сайта
        browser.open(WEB_URL)  # Открываем нашу страницу заного, чтобы куки применились

    with allure.step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN)) #сверяем, что появился логин на странице
        time.sleep(5)