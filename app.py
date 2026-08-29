"""
app.py with JWT in cookies
--------------------------
Main Streamlit entry point with JWT:
- Signup and login flows
- JWT token generation and verification
- Role-based dashboards (admin vs user)
- Stores JWT in secure cookie
- Persists login across browser sessions
- Handles token expiry and auto-logout
- 'Remember Me' option for longer sessions
- Sidebar shows countdown + progress bar (color-coded)
"""

import streamlit as st
import jwt
import datetime
from db.db_setup import SessionLocal
from db.models import User
from auth.auth_utils import hash_password, verify_password
from pages.admin_dashboard import admin_dashboard
from pages.user_dashboard import user_dashboard
from streamlit_cookies_manager import EncryptedCookieManager
from pages.logs_dashboard import logs_dashboard

# --- JWT Config ---
SECRET_KEY = "supersecretkey"  # 🔒 replace with env variable in production

# --- Cookie Manager ---
cookies = EncryptedCookieManager(
    prefix="gatekeeper",  # cookie namespace
    password="anothersecretkey",  # 🔒 encryption key
)

if not cookies.ready():
    st.stop()


def create_jwt(username: str, role: str, remember_me: bool = False):
    """
    Create a JWT token for the authenticated user.
    - Includes username and role in the payload
    - Expiry: 1 hour if not remembered, 7 days if 'Remember Me' checked
    - Encodes payload using HS256 algorithm and SECRET_KEY
    """
    expiry = datetime.timedelta(days=7) if remember_me else datetime.timedelta(hours=1)
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + expiry,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_jwt(token: str):
    """
    Decode and validate a JWT token.
    - Verifies signature using SECRET_KEY
    - Returns payload if valid
    - Handles expired tokens (auto-logout)
    - Handles invalid tokens (clears session)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        st.error("❌ Token expired. Please log in again.")
        cookies["jwt_token"] = ""  # clear cookie on expiry
        return None
    except jwt.InvalidTokenError:
        st.error("❌ Invalid token.")
        cookies["jwt_token"] = ""  # clear cookie on invalid token
        return None


# --- Signup Flow ---
def signup(username: str, password: str, role: str = "user"):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter_by(username=username).first()
        if existing_user:
            st.error("❌ Username already exists")
            return
        hashed_pw = hash_password(password)
        new_user = User(username=username, password_hash=hashed_pw, role=role)
        db.add(new_user)
        db.commit()
        st.success(f"✅ User '{username}' created successfully!")
    finally:
        db.close()


# --- Login Flow ---
def login(username: str, password: str, remember_me: bool = False):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            st.error("❌ User not found")
            return None
        if verify_password(password, user.password_hash):
            token = create_jwt(user.username, user.role, remember_me)
            cookies["jwt_token"] = token  # store JWT in cookie
            st.success(f"✅ Login successful! Welcome, {user.username} ({user.role})")
            return user
        else:
            st.error("❌ Invalid password")
            return None
    finally:
        db.close()


# --- Logout Flow ---
def logout():
    cookies["jwt_token"] = ""  # clear cookie
    st.info("👋 You have been logged out.")


# --- Session Check ---
def is_authenticated():
    token = cookies.get("jwt_token")
    if token:
        payload = decode_jwt(token)
        if payload:
            return payload
    return None


# --- Streamlit UI ---
def main():
    # --- UI Config ---
    # Sets app title, icon, and layout for a polished look
    st.set_page_config(page_title="Gatekeeper App", page_icon="🔐", layout="centered")
    st.title("🔐 Gatekeeper Authentication System")

    payload = is_authenticated()

    if payload:
        # --- Sidebar session info ---
        # Calculate remaining time until JWT expiry
        expiry_time = datetime.datetime.fromtimestamp(payload["exp"])
        remaining = expiry_time - datetime.datetime.utcnow()
        total_seconds = int(remaining.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Progress fraction (max 7 days session length)
        max_session_seconds = 7 * 24 * 3600
        progress_fraction = max(total_seconds, 0) / max_session_seconds

        # Color-coded indicator based on remaining time
        if progress_fraction > 0.5:
            bar_color = "🟢"
        elif progress_fraction > 0.2:
            bar_color = "🟡"
        else:
            bar_color = "🔴"

        # Sidebar display: user info + countdown + color indicator
        st.sidebar.markdown(
            f"**Logged in as:** {payload['username']} ({payload['role']})\n\n"
            f"**Session expires in:** {hours}h {minutes}m {seconds}s {bar_color}"
        )
        st.sidebar.progress(progress_fraction)

        # Logout button
        if st.sidebar.button("🚪 Logout"):
            logout()

        # Role-based dashboards
        if payload["role"] == "admin":
            admin_dashboard()
        else:
            user_dashboard(payload["username"])

    else:
        # --- Authentication menu ---
        st.sidebar.header("🔑 Authentication")
        menu = st.sidebar.radio("Choose an option:", ["Signup 📝", "Login 🔐"])

        if menu.startswith("Signup"):
            st.subheader("📝 Create a New Account")
            # Split form into two columns for cleaner layout
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username")
                role = st.selectbox("Role", ["user", "admin"])
            with col2:
                password = st.text_input("Password", type="password")
            if st.button("✅ Signup"):
                signup(username, password, role)

        elif menu.startswith("Login"):
            st.subheader("🔐 Login to Your Account")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            remember_me = st.checkbox("Remember Me")  # ✅ new option
            if st.button("🚀 Login"):
                login(username, password, remember_me)


if __name__ == "__main__":
    main()
