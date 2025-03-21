from datetime import datetime, timezone
from datetime import timedelta

import jwt

SECRET_KEY = "BuzeBSecret!@"
ALGORITHM = "HS256"
INVALID_TOKEN = "Invalid token"
TOKEN_EXPIRED = "Token has expired"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200


def _get_expiration_time_for(expiration_min):
    expire = (datetime.now(timezone.utc) + timedelta(
        minutes=expiration_min))
    return expire.timestamp()


class TokenExpiredError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class InvalidTokenError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class TokenHandler:
    def __init__(self):
        self.expires_at = None
        self.access_token = None
        self.token_type = "bearer"

    def generate(self, expiration_in_min=ACCESS_TOKEN_EXPIRE_MINUTES):
        self.expires_at = _get_expiration_time_for(expiration_in_min)
        self.access_token = jwt.encode({"sub": "BuzzMe", "exp": self.expires_at},
                                       SECRET_KEY, algorithm=ALGORITHM)
        return self

    def to_response(self):
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_at": datetime.fromtimestamp(self.expires_at).isoformat()
        }

    @staticmethod
    def verify(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError(TOKEN_EXPIRED)

        except jwt.InvalidTokenError:
            raise InvalidTokenError(INVALID_TOKEN)
