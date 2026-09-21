import allure
import pytest
from helpers.data import INVALID_LOGIN_DATA

@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestUserLogin:
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self, client, registered_user):
        user_payload, _ = registered_user
        response = client.login_user({
            "email": user_payload["email"],
            "password": user_payload["password"],
        })
        body = response.json()
        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"]["email"] == user_payload["email"]
        assert body["user"]["name"] == user_payload["name"]
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @allure.title("Вход с неверным логином и паролем")
    def test_login_with_wrong_credentials_returns_error(self, client):
        response = client.login_user(INVALID_LOGIN_DATA)
        body = response.json()
        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"
