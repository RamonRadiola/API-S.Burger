import requests
from constants import Constants
import allure


@allure.story("Проверяет ручку 'Получение заказов конкретного пользователя'")
class TestGetUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_auth(self, login_user):
        access_token = login_user[2]
        get_orders_response = requests.get(
            Constants.URL_ORDERS,
            headers={"Authorization": access_token}
        )
        response_body = get_orders_response.json()
        assert get_orders_response.status_code == 200
        assert response_body["success"] is True


    @allure.title("Попытка получения заказов неавторизованного пользователя")
    def test_get_user_orders_without_auth(self):
        get_orders_response = requests.get(Constants.URL_ORDERS)
        response_body = get_orders_response.json()
        assert get_orders_response.status_code == 401
        assert response_body["success"] is False
        assert response_body["message"] == "You should be authorised"