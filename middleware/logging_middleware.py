import time
import json
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.concurrency import iterate_in_threadpool
from services.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()
        
        # Get request info
        method = request.method
        url = str(request.url.path)
        query_params = dict(request.query_params)
        client_ip = request.client.host if request.client else "unknown"
        
        # Get request body
        request_body = None
        if method in ["POST", "PUT", "PATCH"]:
            try:
                body_bytes = await request.body()
                if body_bytes:
                    request_body = json.loads(body_bytes.decode())
            except (json.JSONDecodeError, UnicodeDecodeError):
                request_body = "<unable to parse>"
        
        # Log incoming request
        logger.info("INCOMING REQUEST")
        logger.info(f"  Method     : {method}")
        logger.info(f"  Endpoint   : {url}")
        if query_params:
            logger.info(f"  Query      : {json.dumps(query_params, separators=(',', ':'))}")
        if request_body:
            # Mask sensitive data and format inline
            masked_body = self._mask_sensitive(request_body)
            logger.info(f"  Body       : {json.dumps(masked_body, separators=(',', ':'))}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = (time.time() - start_time) * 1000  # Convert to ms
        
        # Get response body
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        
        response_content = None
        try:
            response_content = json.loads(b"".join(response_body).decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            response_content = "<unable to parse>"
        
        # Log response
        status_text = "OK" if response.status_code < 400 else "ERROR"
        logger.info("OUTGOING RESPONSE")
        logger.info(f"  Status     : {response.status_code} {status_text}")
        logger.info(f"  Duration   : {duration:.2f}ms")
        if response_content and response_content != "<unable to parse>":
            masked_response = self._mask_sensitive(response_content)
            logger.info(f"  Body       : {json.dumps(masked_response, separators=(',', ':'))}")
        
        return response
    
    def _mask_sensitive(self, data: dict) -> dict:
        """Mask sensitive fields in logs"""
        if not isinstance(data, dict):
            return data
            
        masked = data.copy()
        sensitive_fields = ['secret_key', 'password', 'token', 'api_key']
        
        for field in sensitive_fields:
            if field in masked:
                value = str(masked[field])
                if len(value) > 4:
                    masked[field] = value[:2] + '*' * (len(value) - 4) + value[-2:]
                else:
                    masked[field] = '****'
        
        return masked
