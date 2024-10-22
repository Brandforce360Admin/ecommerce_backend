import pytest

from tests.common_fixtures import USER_BASE_URL


@pytest.fixture(scope="function")
def register_user_response(client, request):
    response = client.post(f"{USER_BASE_URL}/register", json=request.param)
    return response


@pytest.fixture(scope="class")
def register_teardown_login_delete(client, request):
    register_request, login_request = request.param
    register_response = client.post(f"{USER_BASE_URL}/register", json=register_request)
    yield register_response
    login_response = client.post(f"{USER_BASE_URL}/login", json=login_request)
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    client.delete(f"{USER_BASE_URL}/{login_response.json()["user_details"]["user_id"]}/delete", headers=headers)


@pytest.fixture(scope="function")
def login_user_response(client, request):
    response = client.post(f"{USER_BASE_URL}/login", json=request.param)
    return response
