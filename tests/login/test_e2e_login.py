import pytest
from hamcrest import assert_that, equal_to, is_not
from starlette import status

from tests.support.app_driver import AppDriver


@pytest.fixture(scope='session')
def app():
    app = AppDriver()
    try:
        app.start()
        yield app
    finally:
        app.stop()


def test_login_success(app):
    secret = "TofuMan"
    response = app.login(secret)
    assert_that(response.status_code, equal_to(status.HTTP_200_OK))
    assert_that(response.json()["token"], is_not(None))


def test_login_failure(app):
    secret = "BadLord"
    response = app.login(secret)
    assert_that(response.status_code, equal_to(status.HTTP_401_UNAUTHORIZED))
