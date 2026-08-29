"""
login.py
--------
Handles user login:
- Fetches user from database by username
- Verifies password using bcrypt (via auth_utils.verify_password)
- Issues JWT with short or long expiry depending on 'Remember Me'
- Stores JWT in secure cookie
- Redirects based on role
"""

import streamlit as st
import jwt
import datetime
from db.db_setup import SessionLocal
from db.models import User
from auth.auth_utils import verify_password
from pages.admin_dashboard import admin_dashboard
from pages.user_dashboard import user_dashboard
from streamlit_cookies_manager import EncryptedCookieManager

# --- JWT Config ---
SECRET_KEY = "supersecretkey"  # 🔒 replace with env variable in production

# --- Cookie Manager ---
cookies = EncryptedCookieManager(
    prefix="gatekeeper",
    password="anothersecretkey",
)

if not cookies.ready():
    st.stop()


def login(username: str, password: str, remember_me: bool = False):
    """
    Handles user login:
    - Verifies password
    - Issues JWT with short or long expiry depending on 'Remember Me'
    - Stores JWT in secure cookie
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            st.error("❌ User not found")
            return None

        if verify_password(password, user.password_hash):
            # Expiry: 1 hour if not remembered, 7 days if remembered
            expiry = (
                datetime.timedelta(days=7)
                if remember_me
                else datetime.timedelta(hours=1)
            )
            payload = {
                "username": user.username,
                "role": user.role,
                "exp": datetime.datetime.utcnow() + expiry,
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            cookies["jwt_token"] = token  # store JWT in cookie
            st.success(f"✅ Login successful! Welcome, {user.username} ({user.role})")

            # Redirect based on role
            if user.role == "admin":
                admin_dashboard()
            else:
                user_dashboard(user.username)

            return user
        else:
            st.error("❌ Invalid password")
            return None
    finally:
        db.close()
