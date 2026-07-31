from datetime import datetime, timezone, timedelta

from jose import jwt

from app.config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_SECONDS


def create_access_token(sub: str, email: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "email": email,
        "iat": now,
        "exp": now + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
