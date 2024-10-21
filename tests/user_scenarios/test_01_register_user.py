import pytest

from tests.user_scenarios.common_validations import is_valid_uuid, is_valid_datetime
from tests.user_scenarios.fixtures import register_user_response
from tests.user_scenarios.user_details import user_details


@pytest.mark.parametrize('register_user_response', [user_details["user_no_name"]], indirect=True)
def test_register_user_api_no_name(register_user_response):
    assert register_user_response.status_code == 422


@pytest.mark.parametrize('register_user_response', [user_details["user_no_name"]], indirect=True)
def test_register_user_api_no_email(register_user_response):
    assert register_user_response.status_code == 422


@pytest.mark.parametrize('register_user_response', [user_details["user_no_password"]], indirect=True)
def test_register_user_api_no_password(register_user_response):
    assert register_user_response.status_code == 422


@pytest.mark.parametrize('register_user_response', [user_details["user_invalid_email"]], indirect=True)
def test_register_user_api_invalid_email(register_user_response):
    assert register_user_response.status_code == 422


@pytest.mark.parametrize('register_user_response', [user_details["user_invalid_password"]], indirect=True)
def test_register_user_api_invalid_password(register_user_response):
    assert register_user_response.status_code == 400


@pytest.mark.parametrize('register_user_response', [user_details["user1"]], indirect=True)
def test_register_user_api(register_user_response):
    assert register_user_response.status_code == 200
    assert register_user_response.json()["name"] == user_details["user1"]["name"]
    assert register_user_response.json()["email"] == user_details["user1"]["email"]
    assert is_valid_uuid(register_user_response.json()["user_id"])
    assert is_valid_datetime(register_user_response.json()["created_at"])


@pytest.mark.parametrize('register_user_response', [user_details["user1"]], indirect=True)
def test_register_user_api_existing_user(register_user_response):
    assert register_user_response.status_code == 409
