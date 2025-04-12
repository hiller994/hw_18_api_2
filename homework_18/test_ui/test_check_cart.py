import time

import allure
from selene import browser, have

from homework_18.Data import WEB_URL, LOGIN
from homework_18.api.test_requests import test_add_pc, test_add_notebook, test_add_multiple_products, \
    test_authorization


#test UI test_cart
def test_add_in_cart():
    with allure.step("Add multiple products via API and get shared cookies"):
        cart_cookie = test_add_multiple_products()

    with allure.step("check cart (UI)"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cart_cookie})
        browser.open(WEB_URL + "cart")
        browser.element(".product-name").should(have.text("Simple Computer"))
        #browser.all(".qty-input").should(have.values("1", "2"))  # 1 ПК и 2 ноутбук
        time.sleep(1)

def test_summ_in_cart():
    with allure.step("Add multiple products via API and get shared cookies"):
        cart_cookie = test_add_multiple_products()

    with allure.step("check total summ in cart"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cart_cookie})
        browser.open(WEB_URL + "cart")
        browser.element(".product-price").should(have.text("3980.00"))

def test_auth():
    with allure.step("Add multiple products via API and get shared cookies"):
        auth_cookie = test_authorization()
    with allure.step("add cookie"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": auth_cookie})
        browser.open(WEB_URL)
    with allure.step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN)) #сверяем, что появился логин на странице
        time.sleep(5)

