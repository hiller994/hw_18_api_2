import time

import allure
from selene import browser, have

from homework_18.Data import WEB_URL
from homework_18.test_api.test_requests import test_add_pc, test_add_notebook, test_add_multiple_products


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

