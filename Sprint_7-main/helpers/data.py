from helpers.helper import *
import allure


@allure.step('Получаем тело запроса для регистрации курьера')
def courier_data():
    login, password, first_name = generate_courier_data()
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    return payload

@allure.step( 'Генерируем данные без логина')
def registration_data_without_login():
    data = courier_data()
    data.pop("login")
    return data

@allure.step('Генерируем данные без пароля')
def registration_data_without_password():
    data = courier_data()
    data.pop("password")
    return data

@allure.step('Вносим данные для создания заказа')
def get_order_payload(color):
    return {
    "firstName": "Denis",
    "lastName": "Dude",
    "address": "Babushkina,1",
    "metroStation": 1,
    "phone": "+7 999 999 99 99",
    "rentTime": 3,
    "deliveryDate": "2026-03-10",
    "comment": "Ждем",
    "color": [color]
}


class ErrorText:
    class LoginErrorText:
        NON_EXISTENT_ACC_DATA_ERROR_TEXT = "Учетная запись не найдена"
        EMPTY_LOGIN_PASSWORD_FIELD_ERROR_TEXT = "Недостаточно данных для входа"

    class RegistrationErrorText:
        NOT_ENOUGH_DATA_TO_REG_ERROR_TEXT = "Недостаточно данных для создания учетной записи"
        LOGIN_USED_ERROR_TEXT = 'Этот логин уже используется. Попробуйте другой.'
