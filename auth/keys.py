"""
auth/keys.py
------------
Helper module for managing JWT keys and rotation.
"""

import os
from dotenv import load_dotenv
import jwt

# Load environment variables
load_dotenv()

# Support multiple keys for rotation
SECRET_KEYS = {
    "v1": os.getenv("SECRET_KEY_OLD"),  # optional, for grace period
    "v2": os.getenv("SECRET_KEY_NEW"),  # current active key
}

DEFAULT_KID = "v2"  # always use the newest key for signing


def create_jwt(payload: dict) -> str:
    """
    Create a JWT using the newest key.
    """
    key = SECRET_KEYS[DEFAULT_KID]
    payload["kid"] = DEFAULT_KID
    return jwt.encode(payload, key, algorithm="HS256")


def decode_jwt(token: str) -> dict | None:
    """
    Decode JWT using kid if present, otherwise try all keys.
    """
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        if kid and kid in SECRET_KEYS and SECRET_KEYS[kid]:
            return jwt.decode(token, SECRET_KEYS[kid], algorithms=["HS256"])
        # fallback: try all keys
        for key in SECRET_KEYS.values():
            if not key:
                continue
            try:
                return jwt.decode(token, key, algorithms=["HS256"])
            except jwt.InvalidTokenError:
                continue
    except Exception:
        return None
    return None
