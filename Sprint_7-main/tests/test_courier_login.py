import pytest
from api_methods import ApiMethods
from helpers.data import *


class TestLoginCourier:
    @allure.title('Проверка: курьер может авторизоваться заполнив обязательные поля')
    @allure.description('Ответ 200, тело ответа содержит id курьера')
    def test_login_with_registered_data_returns_200(self, courier):
        login, password, _ = courier

        login_data = {"login": login, "password": password}

        login_response = ApiMethods.login_courier(login_data)

        assert login_response.status_code == 200
        assert "id" in login_response.json()


    @allure.title('Проверка наличия ошибки если неправильно указать логин или пароль/авторизация под несуществующим пользователем ')
    def test_login_with_incorrect_credentials_raises_404(self):
        login_data = {"login": "wrong55login", "password": "wron55password"}
        login_response = ApiMethods.login_courier(login_data)
        assert login_response.status_code == 404
        assert "message" in login_response.json()
        assert login_response.json()["message"] == ErrorText.LoginErrorText.NON_EXISTENT_ACC_DATA_ERROR_TEXT


    @pytest.mark.parametrize("login_data", [{"login": "", "password": ""}])
    @allure.title('Проверка, что система вернёт ошибку, при незаполненном обязательном поле')
    def test_login_without_credentials_in_field_raises_400(self, login_data):
        login_response = ApiMethods.login_courier(login_data)
        assert login_response.status_code == 400
        assert "message" in login_response.json()
        assert login_response.json()["message"] == ErrorText.LoginErrorText.EMPTY_LOGIN_PASSWORD_FIELD_ERROR_TEXT


