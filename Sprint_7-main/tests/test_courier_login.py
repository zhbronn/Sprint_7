import pytest
import allure
from api_methods import ApiMethods
from helpers.data import *
from helpers.helper import generate_random_string


class TestLoginCourier:
    
    @allure.title('Проверка: курьер может авторизоваться')
    @allure.description('Ответ 200, тело ответа содержит id курьера')
    def test_login_with_registered_data_returns_200(self, courier):
        login, password, courier_id = courier
        login_data = {"login": login, "password": password}
        
        login_response = ApiMethods.login_courier(login_data)

        assert login_response.status_code == 200
        assert "id" in login_response.json()

    @allure.title('Проверка ошибки при авторизации с неправильным логином')
    def test_login_with_incorrect_login_returns_404(self, courier):
        _, correct_password, _ = courier
        login_data = {"login": "wrong_login", "password": correct_password}
        
        login_response = ApiMethods.login_courier(login_data)
        
        assert login_response.status_code == 404
        assert login_response.json()["message"] == ErrorText.LoginErrorText.NON_EXISTENT_ACC_DATA_ERROR_TEXT

    @allure.title('Проверка ошибки при авторизации с неправильным паролем')
    def test_login_with_incorrect_password_returns_404(self, courier):
        correct_login, _, _ = courier
        login_data = {"login": correct_login, "password": "wrong_password"}
        
        login_response = ApiMethods.login_courier(login_data)
        
        assert login_response.status_code == 404
        assert login_response.json()["message"] == ErrorText.LoginErrorText.NON_EXISTENT_ACC_DATA_ERROR_TEXT

    @allure.title('Проверка ошибки при авторизации несуществующего пользователя')
    def test_login_with_nonexistent_user_returns_404(self):
        login_data = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        login_response = ApiMethods.login_courier(login_data)
        
        assert login_response.status_code == 404
        assert login_response.json()["message"] == ErrorText.LoginErrorText.NON_EXISTENT_ACC_DATA_ERROR_TEXT

    @pytest.mark.parametrize("login_data, expected_error", [
        ({"login": "", "password": ""}, ErrorText.LoginErrorText.EMPTY_LOGIN_PASSWORD_FIELD_ERROR_TEXT),
        ({"login": "test_login", "password": ""}, ErrorText.LoginErrorText.EMPTY_LOGIN_PASSWORD_FIELD_ERROR_TEXT),
        ({"login": "", "password": "test_password"}, ErrorText.LoginErrorText.EMPTY_LOGIN_PASSWORD_FIELD_ERROR_TEXT)
    ])
    @allure.title('Проверка ошибки при незаполненных обязательных полях')
    def test_login_without_credentials_returns_400(self, login_data, expected_error):
        login_response = ApiMethods.login_courier(login_data)
        
        assert login_response.status_code == 400
        assert login_response.json()["message"] == expected_error