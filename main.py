from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import jwt

from models.schemas import (
    EncryptRequest, 
    DecryptRequest, 
    EncryptResponse, 
    DecryptResponse,
    HealthResponse,
    UUIDResponse,
    JWTEncodeRequest,
    JWTDecodeRequest,
    JWTEncodeResponse,
    JWTDecodeResponse
)
from services.crypto import encrypt_text, decrypt_text
from services.generator import generate_uuid_v4, generate_uuid_v1, encode_jwt, decode_jwt
from middleware import LoggingMiddleware
from services.logger import logger
from datetime import datetime
from middleware.auth_middleware import verify_signature


app = FastAPI(title="Encrypt/Decrypt API")

# Add logging middleware
app.add_middleware(LoggingMiddleware)


# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    # Get first error message
    first_error = errors[0] if errors else {}
    field = first_error.get("loc", ["", "unknown"])[-1]
    msg = first_error.get("msg", "Validation error")
    
    return JSONResponse(
        status_code=400,
        content={
            "responseCode": 400,
            "status": "BAD_REQUEST",
            "message": f"{field}: {msg}"
        }
    )


# Custom exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # If detail is already a dict (our custom format), use it
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    
    # Otherwise, format it
    status_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        500: "INTERNAL_ERROR"
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "responseCode": exc.status_code,
            "status": status_map.get(exc.status_code, "ERROR"),
            "message": exc.detail
        }
    )


# Log startup
logger.info("Encrypt/Decrypt API started successfully!")


@app.get("/")
def root():
    return {
        "responseCode": 200,
        "status": "SUCCESS",
        "message": "Encrypt/Decrypt API",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        responseCode=200,
        status="SUCCESS",
        timestamp=datetime.now().isoformat()
    )


# ==================== ENCRYPT/DECRYPT ====================

@app.post("/encrypt", response_model=EncryptResponse, dependencies=[Depends(verify_signature)])
def encrypt(request: EncryptRequest):
    try:
        result = encrypt_text(request.text, request.secret_key)
        return EncryptResponse(
            responseCode=200,
            status="SUCCESS",
            encrypted_text=result,
            message="Text encrypted successfully"
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "responseCode": 500,
                "status": "INTERNAL_ERROR",
                "message": "Failed to encrypt text"
            }
        )


@app.post("/decrypt", response_model=DecryptResponse, dependencies=[Depends(verify_signature)])
def decrypt(request: DecryptRequest):
    try:
        result = decrypt_text(request.encrypted_text, request.secret_key)
        return DecryptResponse(
            responseCode=200,
            status="SUCCESS",
            decrypted_text=result,
            message="Text decrypted successfully"
        )
    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "responseCode": 400,
                "status": "BAD_REQUEST",
                "message": "Invalid encrypted text or wrong secret key",
                "detail": None
            }
        )


# ==================== UUID GENERATOR ====================

@app.get("/uuid", response_model=UUIDResponse, dependencies=[Depends(verify_signature)])
def get_uuid_v4():
    """Generate UUID v4 (random)"""
    return UUIDResponse(
        responseCode=200,
        status="SUCCESS",
        message="UUID v4 generated successfully",
        uuid=generate_uuid_v4(),
        version="v4"
    )


@app.get("/uuid/v1", response_model=UUIDResponse, dependencies=[Depends(verify_signature)])
def get_uuid_v1():
    """Generate UUID v1 (time-based)"""
    return UUIDResponse(
        responseCode=200,
        status="SUCCESS",
        message="UUID v1 generated successfully",
        uuid=generate_uuid_v1(),
        version="v1"
    )


@app.get("/uuid/v4", response_model=UUIDResponse, dependencies=[Depends(verify_signature)])
def get_uuid_v4_explicit():
    """Generate UUID v4 (random) - explicit endpoint"""
    return UUIDResponse(
        responseCode=200,
        status="SUCCESS",
        message="UUID v4 generated successfully",
        uuid=generate_uuid_v4(),
        version="v4"
    )


# ==================== JWT ====================

@app.post("/jwt/encode", response_model=JWTEncodeResponse, dependencies=[Depends(verify_signature)])
def jwt_encode(request: JWTEncodeRequest):
    """Encode payload to JWT token"""
    try:
        token = encode_jwt(
            payload=request.payload,
            secret_key=request.secret_key,
            expires_in_minutes=request.expires_in_minutes
        )
        return JWTEncodeResponse(
            responseCode=200,
            status="SUCCESS",
            message="JWT token generated successfully",
            token=token,
            expires_in_minutes=request.expires_in_minutes
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "responseCode": 500,
                "status": "INTERNAL_ERROR",
                "message": "Failed to encode JWT",
                "detail": str(e)
            }
        )


@app.post("/jwt/decode", response_model=JWTDecodeResponse, dependencies=[Depends(verify_signature)])
def jwt_decode(request: JWTDecodeRequest):
    """Decode JWT token to payload"""
    try:
        payload = decode_jwt(
            token=request.token,
            secret_key=request.secret_key
        )
        return JWTDecodeResponse(
            responseCode=200,
            status="SUCCESS",
            message="JWT token decoded successfully",
            payload=payload
        )
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={
                "responseCode": 401,
                "status": "UNAUTHORIZED",
                "message": "JWT token has expired"
            }
        )
    except jwt.InvalidTokenError as e:
        return JSONResponse(
            status_code=400,
            content={
                "responseCode": 400,
                "status": "BAD_REQUEST",
                "message": f"Invalid JWT token: {str(e)}"
            }
        )
