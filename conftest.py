import pytest
from helpers import GenDataUser
import requests
from constants import Constants


@pytest.fixture
def reg_user(request):
    data = GenDataUser.generate_data_for_register_new_user()
    register_response = requests.post(Constants.URL_USER_REG, json=data)
    access_token = register_response.json().get("accessToken")
    yield register_response, data, access_token
    requests.delete(Constants.URL_USER_DATA_CHANGE, headers={"Authorization": access_token})


@pytest.fixture
def login_user(reg_user):
    data = reg_user[1]
    response_login = requests.post(Constants.URL_LOGIN, json=data)
    access_token = response_login.json().get("accessToken")
    yield response_login, data, access_token
    requests.delete(Constants.URL_USER_DATA_CHANGE, headers={"Authorization": access_token})

#фикстура для параметризованных тестов
@pytest.fixture(params=[
    ("name", "Newname0990"),
    ("email", "newemail09@example.com")
])
def user_data(request):
    return request.param