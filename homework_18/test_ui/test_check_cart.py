import time

import allure
from selene import browser, have

from homework_18.Data import WEB_URL
from homework_18.test_api.test_requets import test_add_pc


#test UI test_cart
def test_cart():
    with allure.step("add PC to cart (API)"):
        test_add_pc()

    with allure.step("save add pc cookie"):
        cookie = test_add_pc().cookies.get("Nop.customer")

    with allure.step("check cart (UI)"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(WEB_URL + "cart")
        browser.element(".product-name").should(have.text("Simple Computer"))
        time.sleep(1)

