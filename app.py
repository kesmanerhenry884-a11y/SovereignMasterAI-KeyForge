"""
ARCHITECTE — SOVEREIGN KEY FORGE API (app.py)
Sèvè API izole pou jere kreyasyon kle pèmanan nan SQLite.
Sekirite: Master verification via MASTER_ROOT_KEY environment variable sèlman.
Mèt Sistèm: Prophete-Kesmaner Henry
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from sovereign_forge import SovereignKeyForge

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Idantite ak sekrè nwayo pou verifye Mèt la
# SEKIRITE: Chaje depi nan Environment Variables SÈLMAN, pa janm hardcode
MASTER_NAME = os.getenv("SYSTEM_MASTER_NAME", "Prophete-Kesmaner Henry")
ADMIN_SECRET = os.getenv("MASTER_ROOT_KEY", "")
ASSISTANT_NAME = os.getenv("ASSISTANT_IDENTITY", "GrandArchitect")

# Valide ke MASTER_ROOT_KEY egziste nan production
if not ADMIN_SECRET and os.getenv("FLASK_ENV") == "production":
    logger.error("MASTER_ROOT_KEY not set in production environment!")

# Limen motè jenerasyon kle a
forge = SovereignKeyForge()

@app.route('/api/forge-key', methods=['POST'])
def web_forge_endpoint():
    """
    Endpoint pou jenerasyon kle API sekirize.
    Sèl mèt la (via MASTER_ROOT_KEY) ki gen dwa fè sa.
    """
    data = request.json or {}
    user_name = data.get("userName", "")
    secret_sent = data.get("masterRootKey", "")
    client_target = data.get("client", "Guest_User")
    category = data.get("category", "LOGIC")
    
    # Verifikasyon sekirize mèt la via sekrè rasin la
    is_master = (user_name == MASTER_NAME and secret_sent == ADMIN_SECRET)

    if not is_master or not ADMIN_SECRET:
        logger.warning(f"Unauthorized forge attempt from user: {user_name}")
        return jsonify({
            "success": False, 
            "error": "🚫 [Aksè Refize]: Sèl Mèt Prophete-Kesmaner Henry ki gen dwa legal sa a."
        }), 403

    try:
        # Rele modil la pou kreye kle a nan SQLite
        raw_key, key_hash = forge.forge_key(client_target, category)
        
        # PA JANM ekri raw_key la nan log oswa repons detaye
        reply = (f"⚡ **[{ASSISTANT_NAME} - Kle Pèmanan Forje]**:\n"
                 f"• **Kategori Kle:** {category.upper()}\n"
                 f"• **Kle an klè (Bay kliyan an 1 fwa SÈLMAN):** `{raw_key}`\n"
                 f"• **Hash SHA-256 (Sove pou lavi nan SQLite):** `{key_hash}`\n"
                 f"Kòd sa a pare pou idantifye aparèy la otonòm san limit.")

        logger.info(f"Key created for client: {client_target}, category: {category.upper()}")
        
        return jsonify({
            "success": True, 
            "mode": "KEY_CREATED", 
            "orator": ASSISTANT_NAME, 
            "data": reply
        }), 201
    except Exception as e:
        logger.error(f"Error forging key: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@app.route('/api/verify-key', methods=['POST'])
def verify_key_endpoint():
    """
    Endpoint pou verifye kle API.
    Aksesibl pou tout kliyan ki gen valide kle.
    """
    data = request.json or {}
    provided_key = data.get("apiKey", "")
    
    if not provided_key:
        return jsonify({
            "success": False,
            "error": "Kle API a mande"
        }), 400
    
    try:
        key_info = forge.verify_key(provided_key)
        
        if not key_info:
            logger.warning("Invalid key verification attempt")
            return jsonify({
                "success": False,
                "error": "🚫 [Aksè Refize]: Kle sa a pa rekonèt nan brat sekrè a."
            }), 403
        
        return jsonify({
            "success": True,
            "mode": "KEY_VERIFIED",
            "client": key_info["client"],
            "category": key_info["category"],
            "orator": ASSISTANT_NAME
        }), 200
    except Exception as e:
        logger.error(f"Error verifying key: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@app.route('/api/supreme-core', methods=['POST'])
def supreme_core_endpoint():
    """
    Endpoint siprèm pou master oswa kle valide.
    """
    data = request.json or {}
    user_name = data.get("userName", "")
    provided_key = data.get("apiKeyUsed", "")
    
    # Verifye kle a nan SQLite
    key_info = forge.verify_key(provided_key) if provided_key else None
    is_master = (user_name == MASTER_NAME)

    if not is_master and not key_info:
        logger.warning(f"Unauthorized supreme-core access attempt from user: {user_name}")
        return jsonify({
            "success": False, 
            "error": "🚫 [Aksè Refize]: Kle sa a pa rekonèt nan brat sekrè a."
        }), 403

    try:
        key_type = key_info["category"] if key_info else "Kontwòl Dirèk Mèt"
        reply = (f"👑 **[Obeysans Siprèm devan ou, Mèt mwen {MASTER_NAME.upper()}]!**\n\n"
                 f"Nwayo a rekonèt aksè ou via **{key_type}**. Done yo estoke an sekirite nan SQLite pou lavi.\n"
                 f"Asistan pèsonèl ou a pare pou l gouvènen nèt. Di m sa pou n regle, Mèt mwen.")

        return jsonify({
            "success": True, 
            "mode": "MASTER_DOMINATION", 
            "orator": ASSISTANT_NAME, 
            "data": reply
        }), 200
    except Exception as e:
        logger.error(f"Error in supreme-core endpoint: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "🟢 OPERATIONAL", 
        "service": "SovereignKeyForge",
        "database": "SQLITE_PERMANENT_ACTIVE",
        "master": MASTER_NAME,
        "assistant": ASSISTANT_NAME
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "service": "SovereignKeyForge",
        "status": "🟢 ACTIVE",
        "endpoints": {
            "/api/forge-key": "POST - Jenerasyon kle API (Master sèlman)",
            "/api/verify-key": "POST - Verifye kle API",
            "/api/supreme-core": "POST - Aksè siprèm",
            "/health": "GET - Status sèvis la"
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 7860))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)
