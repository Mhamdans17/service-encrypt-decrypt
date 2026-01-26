from cryptography.fernet import Fernet
import base64
import hashlib


def get_fernet_key(secret_key: str) -> bytes:
    hashed = hashlib.sha256(secret_key.encode()).digest()
    return base64.urlsafe_b64encode(hashed)


def encrypt_text(text: str, secret_key: str) -> str:
    key = get_fernet_key(secret_key)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(text.encode())
    return encrypted.decode()


def decrypt_text(encrypted_text: str, secret_key: str) -> str:
    key = get_fernet_key(secret_key)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_text.encode())
    return decrypted.decode()