import pytest
import requests
from constants import Constants
import allure


@allure.story("Проверяет ручку 'Создание пользователя'")
class TestCreateUser:
    @allure.title("Проверка возможности создания уникального пользователя")
    def test_create_unique_user(self, reg_user):
        response = reg_user[0]
        assert 200 == response.status_code


    @allure.title("Проверка на отсутствие возможности регистрации двух одинаковых пользователей")
    def test_no_create_users_with_same_data(self, reg_user):
        data = reg_user[1]
        response_second = requests.post(Constants.URL_USER_REG, json=data)
        get_massage = response_second.json().get("message")
        assert 403 == response_second.status_code
        assert 'User already exists' == get_massage


    @allure.title("Проверка вывода ожидаемого сообщения 'Email, password and name are required fields' при попытке регистрации пользователя без заполнения обязательных полей")
    @pytest.mark.parametrize("field_to_remove", ["email", "password", "name"])
    def test_no_create_user_without_required_fields(self, reg_user, field_to_remove):
        data = reg_user[1].copy()
        data.pop(field_to_remove, None)
        response = requests.post(Constants.URL_USER_REG, json=data)
        assert 403 == response.status_code
        assert response.json()["message"] == "Email, password and name are required fields"

