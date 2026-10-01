"""
ARCHITECTE — Sovereign Key Forge Module (sovereign_forge.py)
Modil otonòm pou jenerasyon, hash SHA-256 ak verifikasyon kle API pa kategori.
Mèt Sistèm: Prophete-Kesmaner Henry
"""

import secrets
import hashlib
import hmac
from typing import Dict, Tuple, Optional

class SovereignKeyForge:
    def __init__(self):
        # Diksyonè lokal sekirize nan memwa RAM
        self._stored_hashes: Dict[str, Dict[str, str]] = {}

    def forge_key(self, client_name: str, category: str) -> Tuple[str, str]:
        """
        Jenere yon kle API sekirize an klè epi kalkile hash li pou stoke li.
        Kategori: LOGIC (Kòd), VISION (Imaj), AUDIO (Vwa), NETWORK (WhatsApp/Rezo)
        """
        category_upper = str(category).upper().strip()
        prefixes = {
            "LOGIC": "sk_logic_",
            "VISION": "sk_vision_",
            "AUDIO": "sk_audio_",
            "NETWORK": "sk_network_"
        }
        
        prefix = prefixes.get(category_upper, "sk_master_")
        
        # Jenerasyon kòd kriptografik inik 64 karaktè hex
        raw_token = secrets.token_hex(32)
        full_api_key = f"{prefix}{raw_token}"
        
        # Kalkile anpwent SHA-256
        key_hash = hashlib.sha256(full_api_key.encode('utf-8')).hexdigest()
        
        # Anrejistre hash la sèlman pou sekirite militè
        self._stored_hashes[key_hash] = {
            "client": client_name,
            "category": category_upper
        }
        
        return full_api_key, key_hash

    def verify_key(self, provided_key: str) -> Optional[Dict[str, str]]:
        """
        Verifye si kle a valab avèk hmac.compare_digest pou evite timing attacks.
        """
        if not isinstance(provided_key, str):
            return None
            
        provided_hash = hashlib.sha256(provided_key.encode('utf-8')).hexdigest()
        
        for stored_hash, info in self._stored_hashes.items():
            if hmac.compare_digest(provided_hash, stored_hash):
                return info
                
        return None
