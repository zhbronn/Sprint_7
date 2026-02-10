import pytest
import allure
from helpers.data import *
from api_methods import ApiMethods


class TestCreateCourier:

    @allure.title('Проверяем, что курьера можно создать')
    @allure.description('Успешный запрос возвращает код 201 и {"ok":true}')
    def test_register_courier_returns_201(self, cleanup_courier):
        data = courier_data()
        login_pass, response = ApiMethods.register_new_courier_and_return_login_password(data)
        
        # Получаем ID курьера для очистки
        if response.status_code == 201:
            login_data = {"login": data["login"], "password": data["password"]}
            login_response = ApiMethods.login_courier(login_data)
            if login_response.status_code == 200:
                courier_id = login_response.json().get("id")
                cleanup_courier.append(courier_id)
        
        assert response.status_code == 201
        assert response.json() == {'ok': True}

    @allure.title('Проверяем, что нельзя создать двух одинаковых курьеров')
    @allure.description('При создании пользователя с существующим логином возвращается ошибка 409')
    def test_register_two_identical_couriers_returns_409(self, cleanup_courier):
        data = courier_data()
        
        # Создаем первого курьера
        login_pass, response_1 = ApiMethods.register_new_courier_and_return_login_password(data)
        
        # Получаем ID первого курьера для очистки
        if response_1.status_code == 201:
            login_data = {"login": data["login"], "password": data["password"]}
            login_response = ApiMethods.login_courier(login_data)
            if login_response.status_code == 200:
                courier_id = login_response.json().get("id")
                cleanup_courier.append(courier_id)
        
        assert response_1.status_code == 201
        assert response_1.json() == {'ok': True}
        
        # Пытаемся создать второго курьера с теми же данными
        _, response_2 = ApiMethods.register_new_courier_and_return_login_password(data)
        
        assert response_2.status_code == 409
        assert "message" in response_2.json()
        assert response_2.json()["message"] == ErrorText.RegistrationErrorText.LOGIN_USED_ERROR_TEXT

    @allure.title('Проверяем ошибку при регистрации без логина')
    def test_register_courier_without_login_returns_400(self, cleanup_courier):
        invalid_data = registration_data_without_login()
        
        _, reg_response = ApiMethods.register_new_courier_and_return_login_password(invalid_data)
        
        # Пытаемся получить ID для очистки на случай бага
        try:
            login_data = {
                "login": invalid_data.get("password", "temp_login"),
                "password": invalid_data.get("password", "temp_pass")
            }
            login_response = ApiMethods.login_courier(login_data)
            if login_response.status_code == 200:
                courier_id = login_response.json().get("id")
                cleanup_courier.append(courier_id)
        except:
            pass
        
        assert reg_response.status_code == 400
        assert "message" in reg_response.json()
        assert reg_response.json()["message"] == ErrorText.RegistrationErrorText.NOT_ENOUGH_DATA_TO_REG_ERROR_TEXT

    @allure.title('Проверяем ошибку при регистрации без пароля')
    def test_register_courier_without_password_returns_400(self, cleanup_courier):
        invalid_data = registration_data_without_password()
        
        _, reg_response = ApiMethods.register_new_courier_and_return_login_password(invalid_data)
        
        # Пытаемся получить ID для очистки на случай бага
        try:
            login_data = {
                "login": invalid_data.get("login", "temp_login"),
                "password": invalid_data.get("firstName", "temp_pass")
            }
            login_response = ApiMethods.login_courier(login_data)
            if login_response.status_code == 200:
                courier_id = login_response.json().get("id")
                cleanup_courier.append(courier_id)
        except:
            pass
        
        assert reg_response.status_code == 400
        assert "message" in reg_response.json()
        assert reg_response.json()["message"] == ErrorText.RegistrationErrorText.NOT_ENOUGH_DATA_TO_REG_ERROR_TEXT