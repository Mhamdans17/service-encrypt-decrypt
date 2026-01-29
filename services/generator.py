import uuid
from datetime import datetime, timedelta
from typing import Optional
import jwt


def generate_uuid_v4() -> str:
    """Generate UUID v4"""
    return str(uuid.uuid4())


def generate_uuid_v1() -> str:
    """Generate UUID v1 (time-based)"""
    return str(uuid.uuid1())


def encode_jwt(
    payload: dict, 
    secret_key: str, 
    expires_in_minutes: Optional[int] = 60,
    algorithm: str = "HS256"
) -> str:
    """Encode data to JWT token"""
    to_encode = payload.copy()
    
    # Add expiration time
    if expires_in_minutes:
        expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        to_encode.update({"exp": expire})
    
    # Add issued at time
    to_encode.update({"iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_jwt(
    token: str, 
    secret_key: str, 
    algorithm: str = "HS256"
) -> dict:
    """Decode JWT token"""
    decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
    return decoded
