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

#Тест API
def test_login_though_api():
    """Successful authorization to some demowebshop (API)"""
    #with allure.step("Open login page"):
    #    browser.open("http://demowebshop.tricentis.com/login")
    #
    #with allure.step("Fill login form"):
    #    browser.element("#Email").send_keys(LOGIN)
    #    browser.element("#Password").send_keys(PASSWORD).press_enter()

    resoult = requests.post(url=API_URL,
                            data= {"Email": LOGIN, "Password": PASSWORD},
                            allow_redirects=False) #ВЫОУЮАЕИ РЕДИРЕКТ, ЧТОБЫ ЗАПРОС АВТОРИЗАЦИИ НЕ СРЕДИРЕКТИЛ, А ОСТАЛСЯ С КОДОМ 302
    print(resoult.status_code)
    print(resoult.text)
    print(resoult.cookies)



    #with allure.step("Verify successful authorization"):
    #    browser.element(".account").should(have.text(LOGIN))