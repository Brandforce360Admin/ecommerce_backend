import pytest

from tests.common_fixtures import register_login_teardown_delete
from tests.common_validations import is_valid_uuid
from tests.test_data.user_data.login_user_user import login_user
from tests.test_data.user_data.register_user import register_user


class TestLoginUser:

    @pytest.mark.parametrize('register_login_teardown_delete',
                             [(register_user["register_user"], login_user["login_user"])],
                             indirect=True)
    def test_login_user_api(self, register_login_teardown_delete):
        register_response, login_response = register_login_teardown_delete
        assert register_response.status_code == 200
        assert login_response.status_code == 200
        assert login_response.json()["user_details"]["name"] == register_user["register_user"]["name"]
        assert login_response.json()["user_details"]["email"] == login_user["login_user"]["email"]
        assert is_valid_uuid(login_response.json()["user_details"]["user_id"])
        assert login_response.json()["access_token"] is not None
