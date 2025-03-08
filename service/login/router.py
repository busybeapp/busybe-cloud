import logging
import uuid
from typing import Dict, Any

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()


ALLOWED_SECRETS = {"Creeper", "EndyBoy", "ZomBoi",
                   "Blazey", "Witherz", "PiglinX",
                   "Ghastly", "EvokerX", "WardenX", "Slimey"}
TOKEN_STORE = {}


class LoginRequest(BaseModel):
    secret: str


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def login(request: LoginRequest):
    if request.secret not in ALLOWED_SECRETS:
        logger.warning("Unauthorized login attempt")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    token = str(uuid.uuid4())
    TOKEN_STORE[token] = request.secret
    logger.info("User logged in successfully")

    return {"token": token}
