from pydantic import BaseModel
from typing import Optional


class BaseResponse(BaseModel):
    responseCode: int
    status: str
    message: str


class EncryptRequest(BaseModel):
    text: str
    secret_key: str


class DecryptRequest(BaseModel):
    encrypted_text: str
    secret_key: str


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
    
