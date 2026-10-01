"""
ARCHITECTE — SOVEREIGN KEY FORGE SERVICE (app.py)
Sèvè Sèvis Kle Dediye - Apa nan nwayo SovereignMasterAI prensipal la.
Mèt Sistèm: Prophete-Kesmaner Henry
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sovereign_forge import SovereignKeyForge

app = Flask(__name__)
CORS(app)

# Idantite Siprèm Nwayo a
MASTER_NAME = os.getenv("SYSTEM_MASTER_NAME", "Prophete-Kesmaner Henry")
ASSISTANT_NAME = os.getenv("ASSISTANT_IDENTITY", "GrandArchitect")
SYSTEM_NAME = "SovereignKeyForge"

# Limen motè jenerasyon kle a
forge = SovereignKeyForge()

@app.route('/api/forge-key', methods=['POST'])
def web_forge_endpoint():
    """
    Endpoint pou jenerasyon kle API sekirize.
    Sèl MASTER_NAME a gen dwa fè sa.
    """
    data = request.json or {}
    message = data.get("message", "")
    user_name = data.get("userName", "")
    client_target = data.get("client", "Guest_User")
    category = data.get("category", "LOGIC")
    
    query = str(message).lower().strip()

    # Se sèl Mèt Henry ki gen dwa bay lòd pou forje kle
    is_master = (user_name == MASTER_NAME or "henry" in query or "kesmaner" in query)

    if not is_master:
        return jsonify({
            "success": False, 
            "error": "🚫 [Aksè Refize]: Sèl Mèt Prophete-Kesmaner Henry ki gen dwa legal sa a."
        }), 403

    # Rele modil sovereign_forge la pou egzekite travay la
    raw_key, key_hash = forge.forge_key(client_target, category)
    
    reply = (f"⚡ **[{ASSISTANT_NAME} - Nwayo Forje Nèf]:**\n"
             f"• **Kategori Kle:** {category.upper()}\n"
             f"• **Kle Sekirite (Montre Kliyan an 1 fwa):** `{raw_key}`\n"
             f"• **Anpwent SHA-256 (Stoke nan database):** `{key_hash}`\n"
             f"Kòd sa a fenk fèt pou idantifye aparèy la otonòm san okenn platfòm deyò.")

    return jsonify({
        "success": True, 
        "mode": "KEY_CREATED", 
        "orator": ASSISTANT_NAME, 
        "data": reply
    }), 201

@app.route('/api/verify-key', methods=['POST'])
def verify_key_endpoint():
    """
    Endpoint pou verifye si yon kle valab.
    """
    data = request.json or {}
    provided_key = data.get("apiKey", "")
    
    if not provided_key:
        return jsonify({
            "success": False, 
            "error": "🚫 Kle API a mande."
        }), 400
    
    key_info = forge.verify_key(provided_key)
    
    if not key_info:
        return jsonify({
            "success": False, 
            "error": "🚫 [Aksè Refize]: Kle sa a pa valid nan brat sekrè a."
        }), 403
    
    return jsonify({
        "success": True, 
        "mode": "KEY_VERIFIED", 
        "client": key_info["client"],
        "category": key_info["category"],
        "orator": ASSISTANT_NAME
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "🟢 OPERATIONAL",
        "service": SYSTEM_NAME,
        "master": MASTER_NAME,
        "assistant": ASSISTANT_NAME
    }), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": SYSTEM_NAME,
        "status": "🟢 ACTIVE",
        "endpoints": {
            "/api/forge-key": "POST - Jenerasyon kle API (MASTER sèlman)",
            "/api/verify-key": "POST - Verifye kle API",
            "/api/health": "GET - Status sèvis la"
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 7860))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)
