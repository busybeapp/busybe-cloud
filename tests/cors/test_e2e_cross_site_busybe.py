import pytest
from hamcrest import assert_that, equal_to
from starlette import status

from service.middleware.cors_enforcer import ALLOWED_ORIGINS
from tests.support.app_driver import AppDriver


@pytest.fixture(scope='session')
def app():
    app = AppDriver()
    try:
        app.start()
        yield app
    finally:
        app.stop()


@pytest.mark.parametrize("origin", ALLOWED_ORIGINS)
def test_allowed_origins(app, origin):
    response = app.is_healthy(headers={"Origin": origin})
    assert_that(response.headers.get("access-control-allow-credentials"),
                equal_to("true"))


def test_not_allow_origin(app):
    response = app.is_healthy(headers={"Origin": "https://unknown-origin.com"})
    assert_that(response.status_code, equal_to(status.HTTP_403_FORBIDDEN))
