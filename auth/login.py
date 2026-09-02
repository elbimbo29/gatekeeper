import streamlit as st
import datetime
from db.db_setup import SessionLocal
from db.models import User
from auth.auth_utils import verify_password
from auth.session_utils import cookies, create_jwt

st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

st.title("🔐 Gatekeeper Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
remember_me = st.checkbox("Remember me")

if st.button("Login"):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            st.error("❌ User not found")
        elif verify_password(password, user.password_hash):
            expiry = (
                datetime.timedelta(days=7)
                if remember_me
                else datetime.timedelta(hours=1)
            )
            payload = {
                "username": user.username,
                "role": user.role,
                "exp": datetime.datetime.now(datetime.UTC) + expiry,
            }

            token = create_jwt(payload)
            cookies["jwt_token"] = token
            cookies.save()

            st.session_state["username"] = user.username
            st.session_state["role"] = user.role
            st.session_state["logged_in"] = True

            st.success(f"✅ Login successful! Welcome, {user.username} ({user.role})")

            # 🔄 Redirect to the correct dashboard
            if user.role == "admin":
                st.switch_page("admin_dashboard")
            else:
                st.switch_page("user_dashboard")

        else:
            st.error("❌ Invalid password")
    finally:
        db.close()
