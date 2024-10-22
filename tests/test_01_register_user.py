import pytest

from tests.common_validations import is_valid_uuid, is_valid_datetime
from tests.test_data.user_data.login_user_user import login_user
from tests.test_data.user_data.register_user import register_user
from tests.user_fixtures import register_user_response, register_teardown_login_delete


class TestRegisterUser:
    @pytest.mark.parametrize('register_user_response', [register_user["register_user_no_name"]], indirect=True)
    def test_register_user_api_no_name(self, register_user_response):
        assert register_user_response.status_code == 422

    @pytest.mark.parametrize('register_user_response', [register_user["register_user_no_name"]], indirect=True)
    def test_register_user_api_no_email(self, register_user_response):
        assert register_user_response.status_code == 422

    @pytest.mark.parametrize('register_user_response', [register_user["register_user_no_password"]], indirect=True)
    def test_register_user_api_no_password(self, register_user_response):
        assert register_user_response.status_code == 422

    @pytest.mark.parametrize('register_user_response', [register_user["register_user_invalid_email"]], indirect=True)
    def test_register_user_api_invalid_email(self, register_user_response):
        assert register_user_response.status_code == 422

    @pytest.mark.parametrize('register_user_response', [register_user["register_user_invalid_password"]], indirect=True)
    def test_register_user_api_invalid_password(self, register_user_response):
        assert register_user_response.status_code == 422

    @pytest.mark.parametrize('register_teardown_login_delete',
                             [(register_user["register_user"], login_user["login_user"])],
                             indirect=True)
    def test_register_user_api(self, register_teardown_login_delete):
        register_response = register_teardown_login_delete
        assert register_response.status_code == 200
        assert register_response.json()["name"] == register_user["register_user"]["name"]
        assert register_response.json()["email"] == register_user["register_user"]["email"]
        assert is_valid_uuid(register_response.json()["user_id"])
        assert is_valid_datetime(register_response.json()["created_at"])

    @pytest.mark.parametrize('register_user_response', [register_user["register_user"]], indirect=True)
    def test_register_user_api_existing_user(self, register_user_response):
        assert register_user_response.status_code == 409
