from fastapi import FastAPI, HTTPException

from models.schemas import (
    EncryptRequest, 
    DecryptRequest, 
    EncryptResponse, 
    DecryptResponse
)
from services.crypto import encrypt_text, decrypt_text
from middleware import LoggingMiddleware
from services.logger import logger
from datetime import datetime


app = FastAPI(title="Encrypt/Decrypt API")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Log startup
logger.info("Encrypt/Decrypt API started successfully!")


@app.get("/")
def root():
    return {"message": "Encrypt/Decrypt API", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/encrypt", response_model=EncryptResponse)
def encrypt(request: EncryptRequest):
    result = encrypt_text(request.text, request.secret_key)
    return EncryptResponse(
        encrypted_text=result,
        message="Text encrypted successfully"
    )


@app.post("/decrypt", response_model=DecryptResponse)
def decrypt(request: DecryptRequest):
    try:
        result = decrypt_text(request.encrypted_text, request.secret_key)
        return DecryptResponse(
            decrypted_text=result,
            message="Text decrypted successfully"
        )
    except Exception:
        raise HTTPException(
            status_code=400, 
            detail="Invalid encrypted text or wrong secret key"
        )


