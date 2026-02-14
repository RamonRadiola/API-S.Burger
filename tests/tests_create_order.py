import requests
from constants import Constants
import allure


@allure.story("Проверяет ручку 'Создание заказа'")
class TestCreateOrder:
    @allure.title("Создание заказа c ингредиентами авторизованным пользователем")
    def test_create_order_with_auth_and_valid_ingredients(self, login_user):
        access_token = login_user[2]
        ingredients_response = requests.get(Constants.URL_INGREDIENTS)
        ingredients = ingredients_response.json()["data"]
        valid_ingredients = [ingredients[0]["_id"], ingredients[1]["_id"]]
        order_data = {"ingredients": valid_ingredients}
        create_order_response = requests.post(
            Constants.URL_ORDERS,
            json=order_data,
            headers={"Authorization": access_token}
        )
        assert create_order_response.status_code == 200
        assert create_order_response.json()["success"] is True



    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        ingredients_response = requests.get(Constants.URL_INGREDIENTS)
        ingredients = ingredients_response.json()["data"]
        valid_ingredients = [ingredients[0]["_id"], ingredients[1]["_id"]]
        order_data = {"ingredients": valid_ingredients}
        create_order_response = requests.post(
            Constants.URL + "/orders",
            json=order_data,
        )
        assert create_order_response.status_code == 200
        assert create_order_response.json()["success"] is True



    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, login_user):
        access_token = login_user[2]
        order_data = {"ingredients": []}
        create_order_response = requests.post(
            Constants.URL_ORDERS,
            json=order_data,
            headers={"Authorization": access_token}
        )
        assert create_order_response.status_code == 400
        assert create_order_response.json()["success"] is False
        assert create_order_response.json()["message"] == "Ingredient ids must be provided"




    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients(self, login_user):
        access_token = login_user[2]
        invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
        order_data = {"ingredients": invalid_ingredients}
        create_order_response = requests.post(
            Constants.URL_ORDERS,
            json=order_data,
            headers={"Authorization": access_token}
        )
        assert create_order_response.status_code == 500