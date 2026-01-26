from pydantic import BaseModel

class EncryptRequest(BaseModel):
    text: str
    secret_key: str

class DecryptRequest(BaseModel):
    encrypted_text: str
    secret_key: str

class EncryptResponse(BaseModel):
    encrypted_text: str
    message: str

class DecryptResponse(BaseModel):
    decrypted_text: str
    message: str
    
