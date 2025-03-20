from hamcrest import assert_that, is_not

INVALID_SECRET = "UnauthorizedSecret"
VALID_SECRET = "Creeper"


def test_login_success(app):
    response_body = app.login(VALID_SECRET)
    assert_that(response_body["access_token"], is_not(None))


def test_login_failure(app):
    app.login(INVALID_SECRET, invalid_secret=True)
