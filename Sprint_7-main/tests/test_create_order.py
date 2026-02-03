import pytest
from api_methods import ApiMethods
from helpers.data import *

class TestCreateOrder:

    @pytest.mark.parametrize("color", ["BLACK", "GREY", "", "BLACK, GREY"])

    @allure.title('Проверка возможности выбора цветов самоката при создании заказа')
    def test_create_order_with_choice_of_color(self, color):
        order_response = ApiMethods.create_order(color)
        assert order_response.status_code == 201
        assert "track" in order_response.json()

