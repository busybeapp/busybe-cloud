import pytest
from hamcrest import not_none
from hamcrest.core import assert_that

from service.login import token
from service.login.token import TokenExpiredError, \
    InvalidTokenError, TOKEN_EXPIRED, INVALID_TOKEN


def test_generate_token():
    token_data = token.generate()
    assert_that(token_data.access_token, not_none())
    assert_that(token_data.expires_at, not_none())


def test_verify_token_expired():
    token_data = token.generate(expiration_in_min=0)
    assert_token_expired(token_data.access_token)


def assert_token_expired(access_token):
    with pytest.raises(TokenExpiredError) as err:
        token.verify(access_token)
    assert_that(str(err.value), TOKEN_EXPIRED)


def test_fail_on_invalid_token():
    invalid_token = "invalid.token.here"
    assert_invalid_token(invalid_token)


def assert_invalid_token(access_token):
    with pytest.raises(InvalidTokenError) as err:
        token.verify(access_token)
    assert_that(str(err.value), INVALID_TOKEN)
