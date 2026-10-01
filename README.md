# 🔐 Sovereign Key Forge

**Autonomous API Key Generation Module for SovereignMasterAI**

---

## 📋 Overview

`SovereignMasterAI-KeyForge` is a dedicated microservice that handles the generation, hashing, and verification of API keys for the SovereignMasterAI ecosystem. This service operates independently from the main SovereignMasterAI core while maintaining secure authentication patterns.

**Master System:** Prophete-Kesmaner Henry  
**Assistant Identity:** GrandArchitect

---

## ⚙️ Features

✅ **SHA-256 Cryptographic Hashing** - Secure key fingerprinting  
✅ **Timing Attack Protection** - Uses `hmac.compare_digest()` for verification  
✅ **Category-Based Keys** - LOGIC, VISION, AUDIO, NETWORK prefixes  
✅ **RAM-Based Storage** - Fast in-memory hash verification  
✅ **Master-Only Access Control** - Authorization via SYSTEM_MASTER_NAME  
✅ **CORS Enabled** - Ready for cross-origin requests  
✅ **Containerized** - Docker & Railway/Render deployment ready  

---

## 🚀 Quick Start

### Local Development

```bash
# Clone and install
git clone https://github.com/kesmanerhenry884-a11y/SovereignMasterAI-KeyForge.git
cd SovereignMasterAI-KeyForge
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run the service
python app.py
```

Service runs on `http://localhost:7860`

### Docker

```bash
docker build -t sovereign-keyforge .
docker run -p 7860:7860 \
  -e SYSTEM_MASTER_NAME="Prophete-Kesmaner Henry" \
  -e ASSISTANT_IDENTITY="GrandArchitect" \
  sovereign-keyforge
```

---

## 📡 API Endpoints

### 1. Generate API Key
**POST** `/api/forge-key`

**Request:**
```json
{
  "userName": "Prophete-Kesmaner Henry",
  "client": "ClientName",
  "category": "LOGIC",
  "message": "forge new key"
}
```

**Response (201):**
```json
{
  "success": true,
  "mode": "KEY_CREATED",
  "orator": "GrandArchitect",
  "data": "⚡ **[GrandArchitect - Nwayo Forje Nèf]:..."  
}
```

---

### 2. Verify API Key
**POST** `/api/verify-key`

**Request:**
```json
{
  "apiKey": "sk_logic_<hex_token>"
}
```

**Response (200):**
```json
{
  "success": true,
  "mode": "KEY_VERIFIED",
  "client": "ClientName",
  "category": "LOGIC",
  "orator": "GrandArchitect"
}
```

---

### 3. Health Check
**GET** `/api/health`

**Response:**
```json
{
  "status": "🟢 OPERATIONAL",
  "service": "SovereignKeyForge",
  "master": "Prophete-Kesmaner Henry",
  "assistant": "GrandArchitect"
}
```

---

## 🔐 Security Notes

- ⚠️ **RAM-Based Storage**: Keys are stored only as SHA-256 hashes in RAM. After restart, all keys are cleared. For production, integrate with a persistent database.
- ⚠️ **Master-Only Creation**: Only requests with `userName == SYSTEM_MASTER_NAME` can create new keys.
- ✅ **No Key Logging**: Raw keys never logged; only hashes stored internally.
- ✅ **Timing Attack Prevention**: Uses `hmac.compare_digest()` for constant-time comparison.

---

## 🌍 Deployment

### Render

1. Connect GitHub repository
2. Set environment variables in Render dashboard:
   - `SYSTEM_MASTER_NAME=Prophete-Kesmaner Henry`
   - `ASSISTANT_IDENTITY=GrandArchitect`
3. Deploy using `render.yaml`

### Railway

1. Connect GitHub repository
2. Railway auto-detects `railway.json`
3. Set environment variables in Railway dashboard
4. Deploy

---

## 📝 Environment Variables

```bash
FLASK_ENV=production              # Flask mode
DEBUG=False                       # Debug mode
PORT=7860                         # Service port
SYSTEM_MASTER_NAME=...            # Master identity
ASSISTANT_IDENTITY=GrandArchitect # Assistant name
SOVEREIGN_OPENAI_CORE=...         # (Optional) OpenAI integration key
SOVEREIGN_GEMINI_CORE=...         # (Optional) Gemini integration key
GRAND_ARCHITECT_KEY=...           # (Optional) Architect key
```

---

## 🔗 Integration with SovereignMasterAI

This service operates independently but can be called by SovereignMasterAI:

```python
import requests

# Generate key
response = requests.post(
    'https://sovereign-keyforge.onrender.com/api/forge-key',
    json={
        'userName': 'Prophete-Kesmaner Henry',
        'client': 'MyClient',
        'category': 'LOGIC'
    }
)

# Verify key
response = requests.post(
    'https://sovereign-keyforge.onrender.com/api/verify-key',
    json={'apiKey': 'sk_logic_<token>'}
)
```

---

## 📞 Support

**Master System:** Prophete-Kesmaner Henry  
**Repository:** https://github.com/kesmanerhenry884-a11y/SovereignMasterAI-KeyForge  
**Main Project:** https://github.com/kesmanerhenry884-a11y/SovereignMasterAI

---

**Status:** 🟢 OPERATIONAL  
**Last Updated:** 2026
