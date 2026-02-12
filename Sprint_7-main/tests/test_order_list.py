import allure
from api_methods import ApiMethods

class TestOrderList:

    @allure.title('Проверяем, что в теле ответа возвращается список заказов')
    @allure.description('В теле ответа содержится ключ "orders" и его значение это список')
    def test_get_order_list(self):
        response = ApiMethods.get_order_list()
        assert response.status_code == 200
        assert "orders" in response.json() and type(response.json()['orders']) == list and "orders" is not None