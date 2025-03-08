import pytest
from fastapi import HTTPException
from hamcrest.core import assert_that
from starlette import status

from service.login.auth_hub import create_token, verify_token


def test_verify_token_success():
    token = create_token("user123")
    verify_token(token)


def test_verify_token_expired():
    expired_token = create_token("user123", 0)
    err = assert_unauthorized_token(expired_token)
    assert_that(err.value.detail, "Token expired")


def assert_unauthorized_token(expired_token):
    with pytest.raises(HTTPException) as err:
        verify_token(expired_token)
    assert_that(err.value.status_code, status.HTTP_401_UNAUTHORIZED)
    return err


def test_verify_token_invalid():
    invalid_token = "invalid.token.here"
    err = assert_unauthorized_token(invalid_token)
    assert_that(err.value.detail, "Invalid token")
