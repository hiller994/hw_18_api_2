import json
import logging
import time

import allure
from allure_commons.types import AttachmentType
from selene import browser, have
import requests

from homework_18.Data import API_URL, MODEL_NOTEBOOK, MODEL_PC, WEB_URL

def add_product_to_cart(url, **kwargs):
    with allure.step("API Request"):
        result = requests.post(url=API_URL + url, **kwargs)
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response", attachment_type=AttachmentType.JSON, extension="json")
        logging.info(result.request.url)
        logging.info(result.status_code)
        logging.info(result.text)
    return result

#test API add_notebook
def test_add_notebook():
    with allure.step("add notebook to cart"):
        response = add_product_to_cart(f'/addproducttocart/details/{MODEL_NOTEBOOK}/1', data={
            "addtocart_31.EnteredQuantity": 2
        })
        assert response.status_code == 200
        return response

#test API add_pc
def test_add_pc():
    with allure.step("add PC to cart"):
        response = add_product_to_cart(f'/addproducttocart/details/{MODEL_PC}/1', data={
                "product_attribute_75_5_31": 96,
                "product_attribute_75_6_32": 100,
                "product_attribute_75_3_33": 102,
                "addtocart_75.EnteredQuantity": 1
            })
        assert response.status_code == 200
        return response