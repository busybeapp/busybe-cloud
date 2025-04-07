import logging
from typing import Dict, Any

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from service.login import token

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_SECRETS = {"Creeper", "EndyBoy", "ZomBoi",
                   "Blazey", "Witherz", "PiglinX",
                   "Ghastly", "EvokerX", "WardenX", "Slimey"}

TOKEN_STORE = set()

UNAUTHORIZED = "Unauthorized"


class LoginRequest(BaseModel):
    secret: str


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def login(request: LoginRequest):
    validate_secret(request.secret)
    token_data = token.generate()
    TOKEN_STORE.add(token_data.access_token)
    return token_data.to_response()


def validate_secret(secret):
    if secret not in ALLOWED_SECRETS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=UNAUTHORIZED)
