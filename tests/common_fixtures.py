import pytest

from app.core.config import settings

BASE_URL = settings.BASE_URL
USER_BASE_URL = f"{BASE_URL}/v1/users"


@pytest.fixture(scope="class")
def register_login_teardown_delete(client, request):
    register_request, login_request = request.param
    register_response = client.post(f"{USER_BASE_URL}/register", json=register_request)
    login_response = client.post(f"{USER_BASE_URL}/login", json=login_request)
    yield register_response, login_response
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    client.delete(f"{USER_BASE_URL}/{login_response.json()["user_details"]["user_id"]}/delete", headers=headers)
