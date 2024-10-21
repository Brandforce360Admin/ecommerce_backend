import pytest

from app.core.config import settings

BASE_URL = settings.BASE_URL
USER_BASE_URL = f"{BASE_URL}/v1/users"


@pytest.fixture(scope="function")
def register_user_response(client, request):
    response = client.post(f"{USER_BASE_URL}/register", json=request.param)
    return response


@pytest.fixture(scope="function")
def login_user_response(client, request):
    response = client.post(f"{USER_BASE_URL}/login", json=request.param)
    return response
