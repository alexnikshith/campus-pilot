import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple, Union
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.hash import argon2

from app.core.config import settings
from app.core.exceptions import UnauthorizedException, ValidationException

# Initialize Argon2id password hasher with recommended modern memory and iteration parameters
argon2_hasher = argon2.using(type="ID", memory_cost=65536, time_cost=3, parallelism=2)

def get_password_hash(password: str) -> str:
    """Hashes a plaintext password using Argon2id."""
    return argon2_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Safely verifies a plaintext password against an Argon2id hash."""
    try:
        return argon2_hasher.verify(plain_password, hashed_password)
    except Exception:
        return False

def validate_password_strength(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validates password strength according to modern security guidelines:
    - Minimum 8 characters
    - At least one uppercase letter (A-Z)
    - At least one lowercase letter (a-z)
    - At least one numeric digit (0-9)
    - At least one special character (!@#$%^&*...)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one numeric digit."
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return False, "Password must contain at least one special character (e.g. !@#$%^&*)."
    return True, None

def create_access_token(
    subject: Union[str, int],
    claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Encodes and signs a JSON Web Token (JWT) with standard and custom claims.
    Standard claims included: sub (string identifier), iat, exp, type="access".
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access"
    }

    if claims:
        to_encode.update(claims)

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodes and verifies a JWT token.
    Raises UnauthorizedException with clean message if expired or malformed.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_type = payload.get("type")
        if token_type != "access":
            raise UnauthorizedException("Invalid token type. Access token expected.")
        return payload
    except ExpiredSignatureError:
        raise UnauthorizedException("Authentication token has expired. Please log in again.")
    except JWTError:
        raise UnauthorizedException("Could not validate credentials. Malformed or invalid token.")

