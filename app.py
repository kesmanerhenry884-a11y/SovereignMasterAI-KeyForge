"""Isolated Flask API for Sovereign Key Forge."""

import logging
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sovereign_forge import SovereignKeyForge

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

MASTER_NAME = os.getenv("SYSTEM_MASTER_NAME", "Prophete-Kesmaner Henry")
ASSISTANT_NAME = os.getenv("ASSISTANT_IDENTITY", "GrandArchitect")
MASTER_ROOT_KEY = os.getenv("MASTER_ROOT_KEY", "")
forge = SovereignKeyForge()


def master_authorized(data: dict) -> bool:
    # The root secret is read from the deployment environment only.
    return bool(MASTER_ROOT_KEY) and data.get("userName") == MASTER_NAME and hmac_compare(
        data.get("masterRootKey", ""), MASTER_ROOT_KEY
    )


def hmac_compare(provided: str, expected: str) -> bool:
    import hmac
    return hmac.compare_digest(str(provided), str(expected))


@app.post("/api/forge-key")
def forge_key_endpoint():
    data = request.get_json(silent=True) or {}
    if not master_authorized(data):
        logger.warning("Unauthorized key-forge attempt")
        return jsonify({"success": False, "error": "Access denied"}), 403
    try:
        raw_key, key_hash = forge.forge_key(
            data.get("client", "Guest_User"), data.get("category", "LOGIC")
        )
        # The raw key is returned once to the authorized caller and never logged or stored.
        return jsonify({
            "success": True,
            "mode": "KEY_CREATED",
            "orator": ASSISTANT_NAME,
            "apiKey": raw_key,
            "keyHash": key_hash,
        }), 201
    except Exception:
        logger.exception("Key creation failed")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.post("/api/verify-key")
def verify_key_endpoint():
    data = request.get_json(silent=True) or {}
    info = forge.verify_key(data.get("apiKey", ""))
    if not info:
        return jsonify({"success": False, "error": "Invalid key"}), 403
    return jsonify({"success": True, "client": info["client"], "category": info["category"]})


@app.get("/health")
def health():
    return jsonify({"status": "OPERATIONAL", "database": "SQLITE"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "7860")))
