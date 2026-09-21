import requests
import allure
from helpers import urls

class StellarBurgersClient:
    TIMEOUT = 15

    @allure.step("Зарегистрировать пользователя")
    def register_user(self, payload: dict) -> requests.Response:
        return requests.post(urls.REGISTER_USER, json=payload, timeout=self.TIMEOUT)

    @allure.step("Авторизоваться пользователем")
    def login_user(self, payload: dict) -> requests.Response:
        return requests.post(urls.LOGIN_USER, json=payload, timeout=self.TIMEOUT)

    @allure.step("Удалить пользователя")
    def delete_user(self, access_token: str) -> requests.Response:
        return requests.delete(urls.DELETE_USER, headers={"Authorization": access_token}, timeout=self.TIMEOUT)

    @allure.step("Получить список ингредиентов")
    def get_ingredients(self) -> requests.Response:
        return requests.get(urls.INGREDIENTS, timeout=self.TIMEOUT)

    @allure.step("Создать заказ")
    def create_order(self, ingredients: list[str] | None = None, access_token: str | None = None) -> requests.Response:
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        payload = {"ingredients": ingredients} if ingredients is not None else {"ingredients": []}
        return requests.post(urls.ORDERS, json=payload, headers=headers, timeout=self.TIMEOUT)
