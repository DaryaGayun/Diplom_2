import allure
import pytest
from helpers.data import INVALID_INGREDIENT_HASH

@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.title("Создать заказ с авторизацией")
    def test_create_order_with_authorization_success(self, client, registered_user, ingredient_ids):
        _, access_token = registered_user
        response = client.create_order(ingredient_ids, access_token)
        body = response.json()
        assert response.status_code == 200
        assert body["success"] is True
        assert "order" in body
        assert body["order"]["number"]
        assert body["name"]

    @allure.title("Создать заказ без авторизации")
    def test_create_order_without_authorization_success(self, client, ingredient_ids):
        response = client.create_order(ingredient_ids)
        body = response.json()
        assert response.status_code == 200
        assert body["success"] is True
        assert "order" in body
        assert body["order"]["number"]

    @allure.title("Создать заказ с ингредиентами")
    def test_create_order_with_ingredients_success(self, client, ingredient_ids):
        response = client.create_order(ingredient_ids)
        body = response.json()
        assert response.status_code == 200
        assert body["success"] is True
        assert body["name"]
        assert body["order"]["number"]

    @allure.title("Нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients_returns_error(self, client):
        response = client.create_order([])
        body = response.json()
        assert response.status_code == 400
        assert body["success"] is False
        assert body["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиента возвращает 500")
    def test_create_order_with_invalid_ingredient_hash_returns_server_error(self, client):
        response = client.create_order([INVALID_INGREDIENT_HASH])
        assert response.status_code == 500
        assert response.text, "Тело ответа не должно быть пустым"
