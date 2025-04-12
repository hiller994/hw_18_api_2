import json
import logging
import time

import allure
from allure_commons.types import AttachmentType
from selene import browser, have
import requests

from homework_18.Data import API_URL, MODEL_NOTEBOOK, MODEL_PC, WEB_URL, LOGIN, PASSWORD


def send_request(session, url, **kwargs):
    with allure.step("API Request"):
        result = session.post(url=API_URL + url, **kwargs)
        allure.attach(
            body=result.request.url,
            name="Request url",
            attachment_type=AttachmentType.TEXT,
        )

        if result.request.body:
            allure.attach(
                body=json.dumps(result.request.body, indent=4, ensure_ascii=False),
                name="Request body",
                attachment_type=AttachmentType.JSON,
                extension="json",
            )

        #обработка ответа - не пытаемся парсить JSON если это не JSON
        try:
            response_data = result.json()
            allure.attach(
                body=json.dumps(response_data, indent=4, ensure_ascii=False),
                name="Response",
                attachment_type=AttachmentType.JSON,
                extension="json",
            )
        except ValueError:
            allure.attach(
                body=result.text,
                name="Response",
                attachment_type=AttachmentType.TEXT,
                extension="txt",
            )

        logging.info(result.request.url)
        logging.info(result.status_code)
        logging.info(result.text)
    return result

#test API add_notebook
def test_add_notebook(session):
    with allure.step("add notebook to cart"):
        response = send_request(session, f'/addproducttocart/details/{MODEL_NOTEBOOK}/1', data={
            "addtocart_31.EnteredQuantity": 2
        })
        assert response.status_code == 200
        return response

#test API add_pc
def test_add_pc(session):
    with allure.step("add PC to cart"):
        response = send_request(session,f'/addproducttocart/details/{MODEL_PC}/1', data={
                "product_attribute_75_5_31": 96,
                "product_attribute_75_6_32": 100,
                "product_attribute_75_3_33": 102,
                "addtocart_75.EnteredQuantity": 1
            })
        assert response.status_code == 200
        return response

#test API login
def test_login(session):
    with allure.step("test login"):
        response = send_request(session, "/login", data= {
            "Email": LOGIN,
            "Password": PASSWORD,
            "RememberMe": False},
                                allow_redirects=False)
    assert response.status_code == 302
    return response

def test_add_multiple_products():
    session = requests.Session()  # Создаем сессию для сохранения кук
    test_add_pc(session)         # Добавляем ПК (куки сохраняются в сессии)
    test_add_notebook(session)   # Добавляем ноутбук (в той же сессии)
    #test_update_quantity(session)
    return session.cookies.get("Nop.customer")  # Возвращаем актуальные куки

def test_authorization():
    session = requests.Session()
    test_login(session)
    return session.cookies.get("NOPCOMMERCE.AUTH")