import os
from datetime import datetime, timezone
from datetime import timedelta

import jwt
from dotenv import load_dotenv
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = (
    int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))

ALLOWED_SECRETS = {"Creeper", "EndyBoy", "ZomBoi",
                   "Blazey", "Witherz", "PiglinX",
                   "Ghastly", "EvokerX", "WardenX", "Slimey"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

TOKEN_STORE = set()


def generate_token(secret: str, expiration_min=ACCESS_TOKEN_EXPIRE_MINUTES):
    validate_secret(secret)
    token = create_token(expiration_min, secret)
    TOKEN_STORE.add(token)
    return token


def create_token(expiration_min, secret):
    payload = {"sub": "BuzzMe", "exp": (_calculate_expiration(expiration_min))}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def validate_secret(secret):
    if secret not in ALLOWED_SECRETS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")


def _calculate_expiration(expiration_min):
    expire = (datetime.now(timezone.utc) + timedelta(
        minutes=expiration_min))
    return expire


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        is_token_exists(token)
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")


def is_token_exists(token):
    if token not in TOKEN_STORE:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")
