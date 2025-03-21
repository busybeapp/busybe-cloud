import logging
from typing import Dict, Any

from fastapi import APIRouter, status
from pydantic import BaseModel

from service.login.auth_gateway import generate_token

logger = logging.getLogger(__name__)
router = APIRouter()


class LoginRequest(BaseModel):
    secret: str


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def login(request: LoginRequest):
    return generate_token(request.secret).to_response()
