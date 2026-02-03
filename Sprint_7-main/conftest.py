import pytest

from api_methods import ApiMethods
from helpers.data import courier_data


@pytest.fixture
def courier():
    data = courier_data()
    login_pass, reg_response = ApiMethods.register_new_courier_and_return_login_password(data)

    login_data = {
        "login": login_pass[0],
        "password": login_pass[1]
    }

    login_response = ApiMethods.login_courier(login_data)

    courier_id = login_response.json().get("id")

    yield login_pass[0], login_pass[1], courier_id

    del_response = ApiMethods.delete_courier(courier_id)
    assert del_response.status_code == 200
