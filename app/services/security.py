import bcrypt
import jwt
import json
import uuid
from datetime import datetime, timezone, timedelta

from app.core.config import SecurityConfig


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=SecurityConfig.SALT_ROUNDS)
    return bcrypt.hashpw(password.encode(), salt).decode()  # Hashed password


def password_matches(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode(), hashed_password.encode()
    )  # Extract the hash metadata (version, cost and salt) from the hashed password and rehash the incoming password to check if they match


def generate_token(user_data: dict, is_refresh: bool) -> str:
    user_data_str = ""
    try:
        user_data_str = json.dumps(obj=user_data, indent=2)
    except TypeError as e:
        print(f"Encountered the following error while serializing user data: {str(e)}")
        return None
    payload = {"sub": user_data_str}
    payload["exp"] = int(
        (
            datetime.now(timezone.utc)
            + (
                timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRY)
                if not is_refresh
                else timedelta(hours=SecurityConfig.REFRESH_TOKEN_EXPIRY)
            )
        ).timestamp()
    )
    payload["jti"] = str(uuid.uuid4())
    payload["is_refresh"] = is_refresh
    return jwt.encode(
        payload=payload, key=SecurityConfig.JWT_SECRET, algorithm=SecurityConfig.JWT_ALGORITHM
    )  # Returns the encoded JWT token


def decode_token(jwt_token) -> dict | None:
    return jwt.decode(
        jwt=jwt_token, key=SecurityConfig.JWT_SECRET, algorithms=SecurityConfig.JWT_ALGORITHM
    )  # Decodes the token and returns the token's payload
