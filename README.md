# 🔐 Crypto & Token API Service

Layanan API untuk enkripsi/dekripsi teks, generate UUID, dan JWT token management.

## 📋 Spesifikasi

| Item | Detail |
|------|--------|
| **Framework** | FastAPI |
| **Python** | 3.9+ |
| **Enkripsi** | Fernet (AES-128-CBC + HMAC) |
| **JWT** | HS256 |
| **Authentication** | HMAC-SHA256 Signature |

---

## 🚀 Base URL

```
https://api.imtokyodev.cloud
```

---

## 🔑 Authentication

Semua endpoint (kecuali `/health`) membutuhkan header authentication:

| Header | Deskripsi |
|--------|-----------|
| `X-Timestamp` | Unix timestamp (detik) saat request dibuat |
| `X-Signature` | HMAC-SHA256 hash dari `{timestamp}{API_SECRET_KEY}` |

### Cara Generate Signature

```python
import hashlib
import time

timestamp = str(int(time.time()))
api_secret_key = "YOUR_API_SECRET_KEY"

signature = hashlib.sha256(
    f"{timestamp}{api_secret_key}".encode()
).hexdigest()
```

> ⚠️ **Note:** Request akan expired setelah **5 menit** dari timestamp.

---

## 📡 Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "responseCode": 200,
  "status": "SUCCESS",
  "timestamp": "2026-01-29T08:00:00"
}
```

---

## 🔒 Encrypt/Decrypt

### Encrypt Text

```http
POST /encrypt
```

**Request Body:**
```json
{
  "text": "Hello World",
  "secret_key": "my-secret-key-123"
}
```

**Response:**
```json
{
  "responseCode": 200,
  "status": "SUCCESS",
  "message": "Text encrypted successfully",
  "encrypted_text": "gAAAAABl..."
}
```

---

### Decrypt Text

```http
POST /decrypt
```

**Request Body:**
```json
{
  "encrypted_text": "gAAAAABl...",
  "secret_key": "my-secret-key-123"
}
```

**Response:**
```json
{
  "responseCode": 200,
  "status": "SUCCESS",
  "message": "Text decrypted successfully",
  "decrypted_text": "Hello World"
}
```

---

## 🆔 UUID Generator

### Generate UUID v4 (Random)

```http
GET /uuid
GET /uuid/v4
```

**Response:**
```json
{
  "responseCode": 200,
  "status": "SUCCESS",
  "message": "UUID v4 generated successfully",
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "version": "v4"
}
```

---

### Generate UUID v1 (Time-based)

```http
GET /uuid/v1
```

**Response:**
```json
{
  "responseCode": 200,
  "status": "SUCCESS",
  "message": "UUID v1 generated successfully",
  "uuid": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "version": "v1"
}
```

---

## 🎫 JWT Token

### Encode JWT

```http
POST /jwt/encode
```

**Request Body:**
```json
{
  "payload": {
    "user_id": "123",
    "role": "admin"
  },
  "secret_key": "my-jwt-secret",
  "expires_in_minutes": 60
}
```

**Response:**
```json
{
  "responseCode": 200,
  "status": "SUCCESS",
  "message": "JWT token generated successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in_minutes": 60
}
```

---

### Decode JWT

```http
POST /jwt/decode
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "secret_key": "my-jwt-secret"
}
```

**Response (Success):**
```json
{
  "responseCode": 200,
  "status": "SUCCESS",
  "message": "JWT token decoded successfully",
  "payload": {
    "user_id": "123",
    "role": "admin",
    "exp": 1706558400,
    "iat": 1706554800
  }
}
```

**Response (Expired):**
```json
{
  "responseCode": 401,
  "status": "UNAUTHORIZED",
  "message": "JWT token has expired"
}
```

---

## ❌ Error Responses

| responseCode | status | Deskripsi |
|--------------|--------|-----------|
| `200` | SUCCESS | Request berhasil |
| `400` | BAD_REQUEST | Input tidak valid |
| `401` | UNAUTHORIZED | Auth gagal / token expired |
| `500` | INTERNAL_ERROR | Server error |

**Error Response Format:**
```json
{
  "responseCode": 400,
  "status": "BAD_REQUEST",
  "message": "secret_key: String should have at least 1 character"
}
```

---

## 💻 Contoh Penggunaan (Python)

```python
import requests
import hashlib
import time

BASE_URL = "https://api.imtokyodev.cloud"
API_SECRET_KEY = "your-api-secret-key"

def get_auth_headers():
    timestamp = str(int(time.time()))
    signature = hashlib.sha256(
        f"{timestamp}{API_SECRET_KEY}".encode()
    ).hexdigest()
    return {
        "Content-Type": "application/json",
        "X-Timestamp": timestamp,
        "X-Signature": signature
    }

# Encrypt
response = requests.post(
    f"{BASE_URL}/encrypt",
    json={"text": "Hello World", "secret_key": "my-key"},
    headers=get_auth_headers()
)
print(response.json())

# Generate UUID
response = requests.get(
    f"{BASE_URL}/uuid",
    headers=get_auth_headers()
)
print(response.json())

# Encode JWT
response = requests.post(
    f"{BASE_URL}/jwt/encode",
    json={
        "payload": {"user_id": "123"},
        "secret_key": "jwt-secret",
        "expires_in_minutes": 60
    },
    headers=get_auth_headers()
)
print(response.json())
```

---

## 🛠️ Local Development

```bash
# Clone repo
git clone https://github.com/your-username/service-encrypt-decrypt.git
cd service-encrypt-decrypt

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup environment
echo "API_SECRET_KEY=your-secret-key" > .env

# Run server
uvicorn main:app --reload
```

---

## 📁 Struktur Project

```
service-encrypt-decrypt/
├── main.py              # Entry point FastAPI
├── requirements.txt     # Dependencies
├── render.yaml          # Render deployment config
├── .env                 # Environment variables
├── middleware/
│   ├── __init__.py
│   ├── auth_middleware.py    # HMAC signature verification
│   └── logging_middleware.py # Request/response logging
├── models/
│   ├── __init__.py
│   └── schemas.py       # Pydantic models
└── services/
    ├── __init__.py
    ├── crypto.py        # Encrypt/decrypt logic
    ├── generator.py     # UUID & JWT generator
    └── logger.py        # Logging configuration
```

---

## 📄 License

TOKYO DEV.ID
