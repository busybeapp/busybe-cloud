import pytest
from fastapi import HTTPException
from hamcrest.core import assert_that
from starlette import status

from service.login.auth_hub import create_token, verify_token


def test_verify_token_expired():
    expired_token = create_token("user123", 0)

    with pytest.raises(HTTPException) as exc_info:
        verify_token(expired_token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_verify_token_success():
    token = create_token("user123")
    verify_token(token)


def test_verify_token_invalid():
    invalid_token = "invalid.token.here"
    with pytest.raises(HTTPException) as err:
        verify_token(invalid_token)

    assert_that(err.value.status_code, status.HTTP_401_UNAUTHORIZED)
