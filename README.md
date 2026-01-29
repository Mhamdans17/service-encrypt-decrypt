# 🔐 Encrypt/Decrypt API Service

Layanan API untuk enkripsi dan dekripsi teks menggunakan algoritma **Fernet (AES-128-CBC)** dengan HMAC authentication.

## 📋 Spesifikasi

| Item | Detail |
|------|--------|
| **Framework** | FastAPI |
| **Python** | 3.9+ |
| **Enkripsi** | Fernet (AES-128-CBC + HMAC) |
| **Authentication** | HMAC-SHA256 Signature |

---

## 🚀 Base URL

```
https://your-service.onrender.com
```

---

## 🔑 Authentication

Setiap request ke endpoint `/encrypt` dan `/decrypt` membutuhkan header authentication:

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

> ⚠️ **Note:** Request akan expired setelah **5 menit** dari timestamp yang diberikan.

---

## 📡 Endpoints

### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-01-29T08:00:00"
}
```

---

### 2. Encrypt Text

```http
POST /encrypt
```

**Headers:**
```
Content-Type: application/json
X-Timestamp: 1706511600
X-Signature: a1b2c3d4e5f6...
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
  "encrypted_text": "gAAAAABl...",
  "message": "Text encrypted successfully"
}
```

---

### 3. Decrypt Text

```http
POST /decrypt
```

**Headers:**
```
Content-Type: application/json
X-Timestamp: 1706511600
X-Signature: a1b2c3d4e5f6...
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
  "decrypted_text": "Hello World",
  "message": "Text decrypted successfully"
}
```

---

## ❌ Error Responses

| Status Code | Deskripsi |
|-------------|-----------|
| `400` | Invalid encrypted text atau wrong secret key |
| `401` | Missing authentication headers |
| `401` | Invalid signature |
| `401` | Request expired |

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

---

## 💻 Contoh Penggunaan

### Python

```python
import requests
import hashlib
import time

BASE_URL = "https://your-service.onrender.com"
API_SECRET_KEY = "your-api-secret-key"

def get_auth_headers():
    timestamp = str(int(time.time()))
    signature = hashlib.sha256(
        f"{timestamp}{API_SECRET_KEY}".encode()
    ).hexdigest()
    return {
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

# Decrypt
response = requests.post(
    f"{BASE_URL}/decrypt",
    json={"encrypted_text": "gAAAAABl...", "secret_key": "my-key"},
    headers=get_auth_headers()
)
print(response.json())
```

### cURL

```bash
# Generate timestamp dan signature dulu
TIMESTAMP=$(date +%s)
SIGNATURE=$(echo -n "${TIMESTAMP}YOUR_API_SECRET_KEY" | sha256sum | cut -d' ' -f1)

# Encrypt
curl -X POST "https://your-service.onrender.com/encrypt" \
  -H "Content-Type: application/json" \
  -H "X-Timestamp: $TIMESTAMP" \
  -H "X-Signature: $SIGNATURE" \
  -d '{"text": "Hello World", "secret_key": "my-key"}'
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
# atau
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env dan set API_SECRET_KEY

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
    └── logger.py        # Logging configuration
```

---

## 📄 License

TOKYO DEV.ID
