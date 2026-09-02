"""
generate_keys.py
----------------
Utility script to generate secure random keys for JWT and cookies.
"""

import secrets


def generate_key(length: int = 32) -> str:
    """
    Generate a secure random hex key.
    Default length = 32 bytes (64 hex chars).
    """
    return secrets.token_hex(length)


if __name__ == "__main__":
    print("🔑 New SECRET_KEY:", generate_key(32))
    print("🍪 New COOKIE_PASSWORD:", generate_key(32))
