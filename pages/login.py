import streamlit as st
from datetime import datetime, timedelta, timezone

from db.db_setup import SessionLocal
from db.models import User
from auth.auth_utils import verify_password
from auth.session_utils import cookies, create_jwt, logout

st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")


def login_form():
    st.title("🔐 Gatekeeper Login")
    username = st.text_input("Username", key="login_page_username")
    password = st.text_input("Password", type="password", key="login_page_password")
    remember_me = st.checkbox("Remember me", key="login_page_remember")

    if st.button("Login"):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                st.error("❌ User not found")
                return

            if not verify_password(password, user.password_hash):
                st.error("❌ Invalid password")
                return

            expiry = timedelta(days=7) if remember_me else timedelta(hours=1)
            expiry_time = datetime.now(timezone.utc) + expiry
            payload = {
                "username": user.username,
                "role": user.role,
                "exp": int(expiry_time.timestamp()),
            }
            token = create_jwt(payload)

            # Save cookie and session state
            try:
                cookies["jwt_token"] = token
                cookies["role"] = user.role
                cookies.save()
            except Exception:
                st.warning(
                    "⚠️ Could not persist cookies; session will last until browser reload."
                )

            st.session_state["username"] = user.username
            st.session_state["role"] = user.role
            st.session_state["logged_in"] = True

            st.success(f"✅ Login successful! Welcome, {user.username} ({user.role})")

            # Redirect and stop immediately
            if user.role == "admin":
                st.switch_page("pages/admin_dashboard.py")
                st.stop()
            elif user.role == "logs":
                st.switch_page("pages/logs_dashboard.py")
                st.stop()
            elif user.role == "user":
                st.switch_page("pages/user_dashboard.py")
                st.stop()
            else:
                st.error("❌ Unknown role. Logging out...")
                logout()
                st.stop()
        finally:
            db.close()


def main():
    login_form()


if __name__ == "__main__":
    main()
