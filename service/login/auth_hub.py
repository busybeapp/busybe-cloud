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

TOKEN_STORE = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def create_token(secret: str, expiration_min=ACCESS_TOKEN_EXPIRE_MINUTES):
    payload = {"sub": secret, "exp": (_calculate_expiration(expiration_min))}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _calculate_expiration(expiration_min):
    expire = (datetime.now(timezone.utc) + timedelta(
        minutes=expiration_min))
    return expire


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")
