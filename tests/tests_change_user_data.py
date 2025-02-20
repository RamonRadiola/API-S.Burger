import requests
from conftest import reg_user
from constants import Constants
import allure


@allure.story("Проверяет ручку 'Изменение данных о пользователе'")
class TestChangeDataUser:
    @allure.title("Проверка возможности изменения данных пользователя с авторизацией")
    def test_update_user_with_auth(self, login_user, user_data):
        field, value = user_data
        response_login, data, access_token = login_user
        new_data = {field: value}
        requests.patch(Constants.URL_USER_DATA_CHANGE, json=new_data, headers={"Authorization": access_token})
        get_user_response = requests.get(
            Constants.URL_USER_DATA_CHANGE,
            headers={"Authorization": access_token}
        )
        updated_user = get_user_response.json()["user"]
        assert updated_user[field] == value
        assert get_user_response.json()["success"] is True


    @allure.title("Параметризованный тест, проверяющий, что при попытке изменения данных неавторизованным пользоватем, учетные данные не изменяются")
    def test_no_update_user_without_auth(self, reg_user, user_data):
        field, value = user_data
        access_token = reg_user[2]
        new_data = {field: value}
        requests.patch(
            Constants.URL_USER_DATA_CHANGE,
            json=new_data,
        )
        get_user_response = requests.get(
            Constants.URL_USER_DATA_CHANGE,
            headers={"Authorization": access_token}
        )
        updated_user = get_user_response.json()["user"]
        assert updated_user[field] != value


    @allure.title("Параметризованный тест, проверяющий вывод сообщения об ошибке при попытке изменения данных неавторизованного пользователя")
    def test_no_update_user_without_auth_and_massage(self, reg_user, user_data):
        field, value = user_data
        new_data = {field: value}
        update_response = requests.patch(
            Constants.URL_USER_DATA_CHANGE,
            json=new_data,
        )
        response_body = update_response.json()
        assert 401 == update_response.status_code
        assert response_body.get("message") == "You should be authorised"