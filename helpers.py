import allure
from faker import Faker


@allure.story("Генерирует данные для регистрации нового курьера")
class GenDataUser:
    @allure.step("Генерирует данные для регистрации нового пользователя и возвращает их в словарь payload")
    def generate_data_for_register_new_user():
        fake = Faker("en_US")
        email = fake.email()
        password = fake.password(8)
        name = fake.first_name()

        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return payload