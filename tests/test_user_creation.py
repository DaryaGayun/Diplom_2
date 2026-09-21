import allure
import pytest
from helpers.data import unique_user

@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserCreation:
    @allure.title("Создать уникального пользователя")
    def test_create_unique_user_success(self, client, users_for_delete):
        user_payload = unique_user()
        response = client.register_user(user_payload)
        body = response.json()
        users_for_delete.append(body["accessToken"])
        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"]["email"] == user_payload["email"]
        assert body["user"]["name"] == user_payload["name"]
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @allure.title("Нельзя создать пользователя, который уже зарегистрирован")
    def test_create_existing_user_returns_error(self, client, registered_user):
        user_payload, _ = registered_user
        response = client.register_user(user_payload)
        body = response.json()
        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == "User already exists"

    @allure.title("Нельзя создать пользователя без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field_returns_error(self, client, missing_field):
        user_payload = unique_user()
        user_payload.pop(missing_field)
        response = client.register_user(user_payload)
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"
