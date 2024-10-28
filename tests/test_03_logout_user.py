import pytest

from tests.common_fixtures import register_login_teardown_delete, USER_BASE_URL
from tests.test_data.user_data.login_user_user import login_user
from tests.test_data.user_data.register_user import register_user


class TestLogoutUser:

    @pytest.mark.parametrize('register_login_teardown_delete',
                             [(register_user["register_user"], login_user["login_user"])],
                             indirect=True)
    def test_login_user_api(self, client, register_login_teardown_delete):
        register_response, login_response = register_login_teardown_delete
        assert register_response.status_code == 200
        assert login_response.status_code == 200
        headers = {"Authorization": f"Bearer {login_response.json()["tokens"]['access_token']}"}
        logout_response = client.post(f"{USER_BASE_URL}/{login_response.json()["user_details"]["user_id"]}/logout",
                                      headers=headers)
        assert logout_response.status_code == 200