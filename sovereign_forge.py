"""
ARCHITECTE — Sovereign Key Forge Module (sovereign_forge.py)
Persistent SQLite key generation, SHA-256 hashing, and verification.
"""

import hashlib
import hmac
import logging
import secrets
import sqlite3
from typing import Dict, Optional, Tuple

DB_FILE = "forge.db"
logger = logging.getLogger(__name__)


def init_db() -> None:
    """Initialize the local SQLite database."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS keys (
                key_hash TEXT PRIMARY KEY,
                client_name TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


class SovereignKeyForge:
    def __init__(self) -> None:
        init_db()

    def forge_key(self, client_name: str, category: str) -> Tuple[str, str]:
        category_upper = str(category).upper().strip()
        prefixes = {
            "LOGIC": "sk_logic_",
            "VISION": "sk_vision_",
            "AUDIO": "sk_audio_",
            "NETWORK": "sk_network_",
        }
        full_api_key = f"{prefixes.get(category_upper, 'sk_master_')}{secrets.token_hex(32)}"
        key_hash = hashlib.sha256(full_api_key.encode("utf-8")).hexdigest()

        # Store only the hash; never persist the raw API key.
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO keys (key_hash, client_name, category) VALUES (?, ?, ?)",
                (key_hash, client_name, category_upper),
            )
            conn.commit()
        return full_api_key, key_hash

    def verify_key(self, provided_key: str) -> Optional[Dict[str, str]]:
        if not isinstance(provided_key, str) or not provided_key:
            return None
        provided_hash = hashlib.sha256(provided_key.encode("utf-8")).hexdigest()
        with sqlite3.connect(DB_FILE) as conn:
            rows = conn.execute(
                "SELECT client_name, category, key_hash FROM keys"
            ).fetchall()
        for client_name, category, stored_hash in rows:
            if hmac.compare_digest(provided_hash, stored_hash):
                return {"client": client_name, "category": category}
        return None
