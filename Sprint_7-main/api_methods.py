import requests
from helpers.data import *
from helpers.urls import *

class ApiMethods:
    @staticmethod
    @allure.step('Регистрация нового курьера.')
    @allure.description('Возвращает статус ответа и список - логин, пароль и имя')
    def register_new_courier_and_return_login_password(data):
        login_pass = []
        url = URLS.courier_url
        reg_response = requests.post(url, data=data)

        if reg_response.status_code == 201:
            login_pass.append(data["login"])
            login_pass.append(data["password"])
            login_pass.append(data["firstName"])

        return login_pass, reg_response

    @staticmethod
    @allure.step('вход курьера в систему')
    def login_courier(login_data):
        url = URLS.courier_login_url
        response = requests.post(url, json=login_data)
        return response


    @staticmethod
    @allure.step('Метод создания заказа')
    def create_order(color):
        url = URLS.orders_url
        payload = get_order_payload(color)
        order_response = requests.post(url, json=payload)
        return order_response

    @staticmethod
    @allure.step('Метод получение списка заказов')
    def get_order_list():
        url = URLS.orders_url
        response = requests.get(url)
        return response


    @staticmethod
    @allure.step('Метод удаления курьера')
    def delete_courier(courier_id):
        url = f"{URLS.courier_url}/{courier_id}"
        del_response = requests.delete(url)
        return del_response

