from hamcrest import assert_that, equal_to, is_not
from starlette import status


def test_login_success(app):
    response = app.valid_user_login()
    assert_that(response.status_code, equal_to(status.HTTP_200_OK))
    assert_that(response.json()["access_token"], is_not(None))


def test_login_failure(app):
    response = app.unauthorized_user_login()
    assert_that(response.status_code, equal_to(status.HTTP_401_UNAUTHORIZED))
