import pytest
import requests
from constants import Constants
import allure


@allure.story("Проверяет ручку 'Авторизация пользователя'")
class TestCreateUser:
    @allure.title("Проверка логина c передачей валидных данных")
    def test_login_user(self, login_user):
        response_login = login_user[0]
        assert 200 == response_login.status_code
        assert response_login.json()["success"] is True


    @allure.title("Проверка на отсутствие возможности авторизации с одним неправильным обязательным параметром")
    @pytest.mark.parametrize("key_to_modify", ["email", "password"])
    def test_no_login_with_unright_param(self, reg_user, key_to_modify):
        data = reg_user[1]
        modified_data = data.copy()
        modified_data[key_to_modify] += 'a'
        response_login = requests.post(Constants.URL_LOGIN, json=modified_data)
        assert 401 == response_login.status_code
        assert response_login.json()["success"] is False


    @allure.title("проверка на отсутствие возможности авторизации без одного обязательного параметра")
    @pytest.mark.parametrize("key_to_modify", ["email", "password"])
    def test_no_login_without_param(self, reg_user, key_to_modify):
         data = reg_user[1]
         modified_data = data.copy()
         modified_data.pop(key_to_modify)
         response_login = requests.post(Constants.URL_LOGIN, json=modified_data)
         assert 401 == response_login.status_code
         assert response_login.json()["success"] is False