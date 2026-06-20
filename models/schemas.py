from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class BaseResponse(BaseModel):
    responseCode: int
    status: str
    message: str


class EncryptRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to encrypt")
    secret_key: str = Field(..., min_length=1, max_length=256, description="Secret key for encryption")


class DecryptRequest(BaseModel):
    encrypted_text: str = Field(..., min_length=1, max_length=20000, description="Encrypted text to decrypt")
    secret_key: str = Field(..., min_length=1, max_length=256, description="Secret key for decryption")


class EncryptResponse(BaseResponse):
    encrypted_text: Optional[str] = None


class DecryptResponse(BaseResponse):
    decrypted_text: Optional[str] = None


class HealthResponse(BaseModel):
    responseCode: int
    status: str
    timestamp: str


class ErrorResponse(BaseResponse):
    detail: Optional[str] = None


# UUID Schemas
class UUIDResponse(BaseResponse):
    uuid: str
    version: str


# JWT Schemas
class JWTEncodeRequest(BaseModel):
    payload: Dict[str, Any] = Field(..., description="Data payload to encode")
    secret_key: str = Field(..., min_length=1, max_length=256, description="Secret key for JWT signing")
    expires_in_minutes: Optional[int] = Field(60, ge=1, le=525600, description="Token expiration in minutes")


class JWTDecodeRequest(BaseModel):
    token: str = Field(..., min_length=1, max_length=2048, description="JWT token to decode")
    secret_key: str = Field(..., min_length=1, max_length=256, description="Secret key for JWT verification")


class JWTEncodeResponse(BaseResponse):
    token: Optional[str] = None
    expires_in_minutes: Optional[int] = None


class JWTDecodeResponse(BaseResponse):
    payload: Optional[Dict[str, Any]] = None

