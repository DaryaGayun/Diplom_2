from uuid import uuid4

INVALID_LOGIN_DATA = {
    "email": "wrong_user@example.com",
    "password": "wrong_password",
}
INVALID_INGREDIENT_HASH = "60d3b41abdacab0026a733c6_invalid"

def unique_user(prefix: str = "api_test") -> dict:
    uid = uuid4().hex
    return {
        "email": f"{prefix}_{uid}@example.com",
        "password": f"Pass_{uid[:12]}",
        "name": f"User_{uid[:8]}",
    }
