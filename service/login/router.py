import logging
from typing import Dict, Any

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from service.login.auth_hub import create_token

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_SECRETS = {"Creeper", "EndyBoy", "ZomBoi",
                   "Blazey", "Witherz", "PiglinX",
                   "Ghastly", "EvokerX", "WardenX", "Slimey"}


class LoginRequest(BaseModel):
    secret: str


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def login(request: LoginRequest):
    if request.secret not in ALLOWED_SECRETS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    token = create_token(request.secret)
    return {"access_token": token, "token_type": "bearer"}
