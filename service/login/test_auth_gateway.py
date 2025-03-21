from unittest.mock import patch

import pytest
from fastapi import HTTPException
from hamcrest import assert_that, is_, has_item

from service.login.auth_gateway import generate_token, TOKEN_STORE, UNAUTHORIZED, \
    validate_token
from service.login.token_handler import TokenHandler

VALID_SECRET = "Creeper"
UNKNOWN_SECRET = "UnknownSecret"
VALID_TOKEN = "valid_token"
UNKNOWN_TOKEN = "unknown_token"


def mock_token_data(*args, **kwargs):
    return type("TokenData", (), {"access_token": VALID_TOKEN})


@patch.object(TokenHandler, "generate", mock_token_data)
def test_generate_token_with_valid_secret():
    token_data = generate_token(VALID_SECRET)
    assert_that(token_data.access_token, is_(VALID_TOKEN))
    assert_that(TOKEN_STORE, has_item(VALID_TOKEN))


def test_should_raise_unauthorized_on_generate_using_unknown_secret():
    assert_unauthorized(generate_token, UNKNOWN_SECRET)


def test_should_raise_unauthorized_on_validate_using_unknown_token():
    assert_unauthorized(validate_token, UNKNOWN_TOKEN)


def assert_unauthorized(func, arg):
    with pytest.raises(HTTPException) as exc:
        func(arg)
    assert_that(exc.value.status_code, is_(401))
    assert_that(exc.value.detail, is_(UNAUTHORIZED))
