import pytest

from app.core.config import settings

BASE_URL = settings.BASE_URL
USER_BASE_URL = f"{BASE_URL}/v1/users"


@pytest.fixture(scope="class")
def register_login_teardown_delete(client, request):
    register_request, login_request = request.param
    register_response = client.post(f"{USER_BASE_URL}/register", json=register_request)
    assert register_response.status_code == 200
    login_response = client.post(f"{USER_BASE_URL}/login", json=login_request)
    assert login_response.status_code == 200
    yield register_response, login_response
    login2_response = client.post(f"{USER_BASE_URL}/login", json=login_request)
    assert login_response.status_code == 200
    headers = {"Authorization": f"Bearer {login2_response.json()["tokens"]['access_token']}"}
    delete_response = client.delete(f"{USER_BASE_URL}/{login2_response.json()["user_details"]["user_id"]}/delete",
                                    headers=headers)
    assert delete_response.status_code == 200
