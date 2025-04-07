from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from service.login.token import Token

UNAUTHORIZED = "Unauthorized"

ALLOWED_SECRETS = {"Creeper", "EndyBoy", "ZomBoi",
                   "Blazey", "Witherz", "PiglinX",
                   "Ghastly", "EvokerX", "WardenX", "Slimey"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

TOKEN_STORE = set()


def generate_token(secret: str):
    validate_exists(secret, ALLOWED_SECRETS)
    token_data = Token().generate()
    TOKEN_STORE.add(token_data.access_token)
    return token_data


def validate_token(token: str = Depends(oauth2_scheme)):
    validate_exists(token, TOKEN_STORE)
    Token().verify(token)


def validate_exists(key, store):
    if key not in store:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=UNAUTHORIZED)
