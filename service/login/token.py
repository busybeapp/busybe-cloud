from datetime import datetime, timezone
from datetime import timedelta
import jwt

SECRET_KEY = "BuzeBSecret!@"
ALGORITHM = "HS256"
INVALID_TOKEN = "Invalid token"
TOKEN_EXPIRED = "Token has expired"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200


def _calculate_expiration_time(expiration_min):
    expire = (datetime.now(timezone.utc) + timedelta(minutes=expiration_min))
    return expire.timestamp()


class TokenExpiredError(Exception):
    def __init__(self, message=TOKEN_EXPIRED):
        super().__init__(message)


class InvalidTokenError(Exception):
    def __init__(self, message=INVALID_TOKEN):
        super().__init__(message)


class Token:
    def __init__(self, access_token=None, expires_at=None):
        self.access_token = access_token
        self.expires_at = expires_at
        self.token_type = "bearer"

    def to_response(self):
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_at": datetime.fromtimestamp(self.expires_at).isoformat()
        }

    @staticmethod
    def generate(expiration_in_min=ACCESS_TOKEN_EXPIRE_MINUTES):
        expires_at = _calculate_expiration_time(expiration_in_min)
        access_token = jwt.encode({"exp": expires_at}, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=access_token, expires_at=expires_at)

    @staticmethod
    def verify(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()

        except jwt.InvalidTokenError:
            raise InvalidTokenError()
