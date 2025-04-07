import pytest
from hamcrest import not_none
from hamcrest.core import assert_that
from service.login.token import Token, TokenExpiredError, \
    InvalidTokenError, TOKEN_EXPIRED, INVALID_TOKEN


@pytest.fixture(scope='function')
def token_handler():
    handler = Token()
    yield handler


def test_generate_token(token_handler):
    token_data = token_handler.generate()
    assert_that(token_data.access_token, not_none())
    assert_that(token_data.expires_at, not_none())


def test_verify_token_expired(token_handler):
    token_data = token_handler.generate(expiration_in_min=0)
    assert_token_expired(token_handler, token_data.access_token)


def assert_token_expired(token_handler, token):
    with pytest.raises(TokenExpiredError) as err:
        token_handler.verify(token)
    assert_that(str(err.value), TOKEN_EXPIRED)


def test_fail_on_invalid_token(token_handler):
    invalid_token = "invalid.token.here"
    assert_invalid_token(token_handler, invalid_token)


def assert_invalid_token(token_handler, token):
    with pytest.raises(InvalidTokenError) as err:
        token_handler.verify(token)
    assert_that(str(err.value), INVALID_TOKEN)
