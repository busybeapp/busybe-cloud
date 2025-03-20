from datetime import datetime, timezone
from datetime import timedelta

import jwt
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

INVALID_TOKEN = "Invalid token"

TOKEN_EXPIRED = "Token expired"

SECRET_KEY = "BuzeBSecret!@"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

ALLOWED_SECRETS = {"Creeper", "EndyBoy", "ZomBoi",
                   "Blazey", "Witherz", "PiglinX",
                   "Ghastly", "EvokerX", "WardenX", "Slimey"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

TOKEN_STORE = set()


def generate_token(secret: str, expiration_in_min=ACCESS_TOKEN_EXPIRE_MINUTES):
    validate_secret(secret)
    token = _create_token(expiration_in_min, secret)
    TOKEN_STORE.add(token)
    return token


def _create_token(expiration_min, secret):
    payload = {"sub": "BuzzMe", "exp": (_get_expiration_time_for(expiration_min))}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def validate_secret(secret):
    if secret not in ALLOWED_SECRETS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")


def _get_expiration_time_for(expiration_min):
    expire = (datetime.now(timezone.utc) + timedelta(
        minutes=expiration_min))
    return expire


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        validate_token_exists(token)
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=TOKEN_EXPIRED)

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=INVALID_TOKEN)


def validate_token_exists(token):
    if token not in TOKEN_STORE:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=INVALID_TOKEN)
