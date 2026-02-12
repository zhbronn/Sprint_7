import pytest
import allure
from helpers.data import *
from api_methods import ApiMethods


class TestCreateCourier:

    @allure.title('Проверяем успешную регистрацию курьера')
    @allure.description('Успешный запрос возвращает код 201 и {"ok":true}')
    def test_register_courier_returns_201(self, cleanup_courier):
        data = courier_data()
        
        # Регистрируем курьера
        login_pass, response = ApiMethods.register_new_courier_and_return_login_password(data)
        
        # Получаем ID для очистки
        login_data = {"login": data["login"], "password": data["password"]}
        login_response = ApiMethods.login_courier(login_data)
        courier_id = login_response.json().get("id")
        cleanup_courier.append(courier_id)
        
        assert response.status_code == 201
        assert response.json() == {'ok': True}

    @allure.title('Проверяем, что нельзя создать курьера с существующим логином')
    @allure.description('При создании пользователя с существующим логином возвращается ошибка 409')
    def test_register_courier_with_existing_login_returns_409(self, cleanup_courier):
        data = courier_data()
        
        # Создаем первого курьера
        _, response_1 = ApiMethods.register_new_courier_and_return_login_password(data)
        
        # Получаем ID первого курьера для очистки
        login_data = {"login": data["login"], "password": data["password"]}
        login_response = ApiMethods.login_courier(login_data)
        courier_id = login_response.json().get("id")
        cleanup_courier.append(courier_id)
        
        # Пытаемся создать второго курьера с теми же данными
        _, response_2 = ApiMethods.register_new_courier_and_return_login_password(data)
        
        assert response_2.status_code == 409
        assert response_2.json()["message"] == ErrorText.RegistrationErrorText.LOGIN_USED_ERROR_TEXT

    @allure.title('Проверяем ошибку при регистрации без логина')
    def test_register_courier_without_login_returns_400(self):
        invalid_data = registration_data_without_login()
        _, reg_response = ApiMethods.register_new_courier_and_return_login_password(invalid_data)
        
        assert reg_response.status_code == 400
        assert reg_response.json()["message"] == ErrorText.RegistrationErrorText.NOT_ENOUGH_DATA_TO_REG_ERROR_TEXT

    @allure.title('Проверяем ошибку при регистрации без пароля')
    def test_register_courier_without_password_returns_400(self):
        invalid_data = registration_data_without_password()
        _, reg_response = ApiMethods.register_new_courier_and_return_login_password(invalid_data)
        
        assert reg_response.status_code == 400
        assert reg_response.json()["message"] == ErrorText.RegistrationErrorText.NOT_ENOUGH_DATA_TO_REG_ERROR_TEXT