"""
auth_utils.py
-------------
Utility functions for authentication:
- Hashing passwords with bcrypt
- Verifying passwords
"""

import bcrypt


# Hash a plain-text password
def hash_password(plain_password: str) -> str:
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


# Verify a plain-text password against stored hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
