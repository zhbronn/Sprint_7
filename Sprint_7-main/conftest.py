import pytest
from api_methods import ApiMethods
from helpers.data import courier_data
import allure


@pytest.fixture
def courier():
    """Фикстура создания и удаления курьера"""
    with allure.step("Создаем тестового курьера"):
        data = courier_data()
        login_pass, response = ApiMethods.register_new_courier_and_return_login_password(data)
        
        # Логинимся для получения ID (предполагаем, что создание прошло успешно)
        login_data = {"login": data["login"], "password": data["password"]}
        login_response = ApiMethods.login_courier(login_data)
        courier_id = login_response.json().get("id")
        
        yield data["login"], data["password"], courier_id
    
    # Постусловие - удаление курьера
    with allure.step("Удаляем тестового курьера"):
        ApiMethods.delete_courier(courier_id)


@pytest.fixture
def cleanup_courier():
    """Фикстура для удаления курьера по его ID"""
    couriers_to_delete = []
    
    yield couriers_to_delete
    
    # Постусловие - удаляем всех созданных курьеров
    for courier_id in couriers_to_delete:
        ApiMethods.delete_courier(courier_id)