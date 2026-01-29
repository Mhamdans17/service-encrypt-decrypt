from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse

from models.schemas import (
    EncryptRequest, 
    DecryptRequest, 
    EncryptResponse, 
    DecryptResponse,
    HealthResponse
)
from services.crypto import encrypt_text, decrypt_text
from middleware import LoggingMiddleware
from services.logger import logger
from datetime import datetime
from middleware.auth_middelware import verify_signature


app = FastAPI(title="Encrypt/Decrypt API")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

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
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "responseCode": 500,
                "status": "INTERNAL_ERROR",
                "message": "Failed to encrypt text",
                "detail": str(e)
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

