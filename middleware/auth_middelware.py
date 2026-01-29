import hashlib
import time
import os
from fastapi import Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "default-secret")
TIME_TOLERANCE = 300  # 5 menit dalam detik

def verify_signature(request: Request):
    # Skip untuk health check dan root
    if request.url.path in ["/", "/health", "/docs", "/openapi.json"]:
        return
    
    timestamp = request.headers.get("X-Timestamp")
    signature = request.headers.get("X-Signature")
    
    if not timestamp or not signature:
        raise HTTPException(
            status_code=401, 
            detail={
                "responseCode": 401,
                "status": "UNAUTHORIZED",
                "message": "Missing authentication headers"
            }
        )
    
    # Cek timestamp expired
    try:
        request_time = int(timestamp)
        current_time = int(time.time())
        if abs(current_time - request_time) > TIME_TOLERANCE:
            raise HTTPException(
                status_code=401, 
                detail={
                    "responseCode": 401,
                    "status": "UNAUTHORIZED",
                    "message": "Request expired"
                }
            )
    except ValueError:
        raise HTTPException(
            status_code=401, 
            detail={
                "responseCode": 401,
                "status": "UNAUTHORIZED",
                "message": "Invalid timestamp"
            }
        )
    
    # Generate signature dan bandingkan
    expected_signature = hashlib.sha256(
        f"{timestamp}{API_SECRET_KEY}".encode()
    ).hexdigest()
    
    if signature != expected_signature:
        raise HTTPException(
            status_code=401, 
            detail={
                "responseCode": 401,
                "status": "UNAUTHORIZED",
                "message": "Invalid signature"
            }
        )