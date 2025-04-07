import pytest
from hamcrest import assert_that, is_not, is_

from tests.support.client import LoginException

UNAUTHORIZED_ERROR = 401
INVALID_SECRET = "UnauthorizedSecret"
VALID_SECRET = "Creeper"


def test_login_success(app):
    response_body = app.login(VALID_SECRET)
    assert_that(response_body["access_token"], is_not(None))


def test_login_failure(app):
    with pytest.raises(LoginException) as err:
        app.login(INVALID_SECRET)
    assert_that(err.value.status_code, is_(UNAUTHORIZED_ERROR))
