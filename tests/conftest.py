import pytest
from helpers.api_client import StellarBurgersClient
from helpers.data import unique_user

@pytest.fixture
def client() -> StellarBurgersClient:
    return StellarBurgersClient()

@pytest.fixture
def users_for_delete(client):
    tokens = []
    yield tokens
    for token in tokens:
        client.delete_user(token)
        
@pytest.fixture
def registered_user(client):
    user_payload = unique_user()
    response = client.register_user(user_payload)
    access_token = response.json()["accessToken"]
    yield user_payload, access_token
    client.delete_user(access_token)

@pytest.fixture
def ingredient_ids(client) -> list[str]:
    response = client.get_ingredients()
    body = response.json()
    return [item["_id"] for item in body["data"][:2]]
