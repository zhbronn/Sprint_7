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
        courier_id = None
        
        # Получаем ID курьера для последующего удаления
        if response.status_code == 201:
            login_data = {"login": data["login"], "password": data["password"]}
            login_response = ApiMethods.login_courier(login_data)
            if login_response.status_code == 200:
                courier_id = login_response.json().get("id")
        
        yield data["login"], data["password"], courier_id
    
    # Постусловие - удаление курьера БЕЗ assert
    if courier_id:
        with allure.step("Удаляем тестового курьера"):
            ApiMethods.delete_courier(courier_id)


@pytest.fixture
def cleanup_courier():
    """Фикстура для удаления курьера по его данным"""
    couriers_to_delete = []
    
    yield couriers_to_delete
    
    # Постусловие - удаляем всех созданных курьеров
    for courier_id in couriers_to_delete:
        if courier_id:
            ApiMethods.delete_courier(courier_id)
