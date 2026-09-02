import streamlit as st
from datetime import datetime, timedelta, timezone
import logging

from db.db_setup import SessionLocal
from db.models import User
from auth.auth_utils import verify_password, hash_password
from auth.session_utils import cookies, create_jwt, decode_jwt, clear_token

# Optional theme component; if missing, comment out or replace
try:
    from components.theme import apply_theme

    apply_theme(default="Dark")
except Exception:
    pass

st.set_page_config(page_title="Gatekeeper", page_icon="🔐", layout="wide")
logging.basicConfig(level=logging.INFO)


def show_login_signup():
    """
    Main authentication UI shown in the page body.
    Keeps Login / Signup radio in the main column only and uses unique keys.
    """
    db = SessionLocal()
    st.info("🚀 Sign up or log in to access your dashboards.")

    # Authentication radio stays in the main column only and uses a unique key
    auth_choice = st.radio(
        "Authentication", ["Login", "Signup"], key="auth_choice_main", horizontal=True
    )

    if auth_choice == "Login":
        st.subheader("🔐 Login")
        username = st.text_input("Username", key="login_username_main")
        password = st.text_input("Password", type="password", key="login_password_main")
        remember_me = st.checkbox("Remember me (7 days)", key="remember_me_main")

        if st.button("🚀 Login", key="login_button_main"):
            user = db.query(User).filter(User.username == username).first()
            if not user:
                st.error("❌ User not found")
                db.close()
                return

            if not verify_password(password, user.password_hash):
                st.error("❌ Invalid password")
                db.close()
                return

            expiry = timedelta(days=7) if remember_me else timedelta(hours=1)
            expiry_time = datetime.now(timezone.utc) + expiry
            payload = {
                "username": user.username,
                "role": user.role,
                "exp": int(expiry_time.timestamp()),
            }
            token = create_jwt(payload)

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

            logging.info("User %s logged in (role=%s)", user.username, user.role)
            st.success(f"✅ Login successful! Welcome, {user.username} ({user.role})")
            st.info("Use the sidebar to open the appropriate dashboard.")
            db.close()
            return

    else:
        st.subheader("📝 Create a New Account")
        new_username = st.text_input("New Username", key="signup_username_main")
        new_password = st.text_input(
            "Password", type="password", key="signup_password_main"
        )
        role = st.selectbox("Role", ["user", "admin", "logs"], key="signup_role_main")
        if st.button("✅ Signup", key="signup_button_main"):
            existing = db.query(User).filter(User.username == new_username).first()
            if existing:
                st.error("❌ Username already exists.")
            else:
                new_user = User(
                    username=new_username,
                    password_hash=hash_password(new_password),
                    role=role,
                )
                db.add(new_user)
                db.commit()
                st.success("✅ Signup successful! Please log in.")
                logging.info("New user %s signed up with role %s", new_username, role)
                db.close()
                return

    db.close()


def header_bar():
    """
    Top header showing current user and a logout button.
    Logout clears token and reruns the app to show login UI.
    """
    username = st.session_state.get("username", "Guest")
    role = st.session_state.get("role", "unknown")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("## 🔐 Gatekeeper")
        st.markdown(f"**User:** {username} | **Role:** {role}")
    with col2:
        if st.button("Logout", key="header_logout"):
            try:
                clear_token()
            except Exception:
                logging.exception("Failed to clear token on logout.")
            st.success("Logged out")
            st.experimental_rerun()


def sidebar_navigation():
    """
    Sidebar navigation. Uses unique keys to avoid collisions with main UI.
    All switches are followed by st.stop() to prevent further execution.
    """
    st.sidebar.markdown("### Navigation")
    if st.sidebar.button("Login Page", key="sidebar_login_page"):
        st.switch_page("pages/login.py")
        st.stop()

    if st.sidebar.button("Admin Dashboard", key="sidebar_admin"):
        st.switch_page("pages/admin_dashboard.py")
        st.stop()

    if st.sidebar.button("User Dashboard", key="sidebar_user"):
        st.switch_page("pages/user_dashboard.py")
        st.stop()

    if st.sidebar.button("Logs Dashboard", key="sidebar_logs"):
        st.switch_page("pages/logs_dashboard.py")
        st.stop()

    st.sidebar.markdown("---")
    st.sidebar.markdown("Theme")
    st.sidebar.radio("Theme", ["Dark", "Light"], index=0, key="sidebar_theme")


def main():
    st.title("Gatekeeper — Landing")
    st.write(
        "This is the landing page. Use the sidebar to navigate to dashboards after login."
    )

    # Render sidebar navigation (keeps left menu consistent)
    sidebar_navigation()

    # Try to read token from cookies; if present and valid, populate session_state
    token = None
    try:
        token = cookies.get("jwt_token")
    except Exception:
        token = None

    if token:
        try:
            payload = decode_jwt(token)
        except Exception:
            payload = None

        if payload:
            st.session_state["username"] = payload.get("username")
            st.session_state["role"] = payload.get("role")
            st.session_state["logged_in"] = True

            header_bar()

            st.markdown("### Quick open")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Open Admin Dashboard", key="quick_admin"):
                    st.switch_page("pages/admin_dashboard.py")
                    st.stop()
            with col2:
                if st.button("Open Logs Dashboard", key="quick_logs"):
                    st.switch_page("pages/logs_dashboard.py")
                    st.stop()
            with col3:
                if st.button("Open User Dashboard", key="quick_user"):
                    st.switch_page("pages/user_dashboard.py")
                    st.stop()

            st.markdown("---")
            st.write(
                "If a dashboard looks broken, logout and log back in. Clear cookies if needed."
            )
            return

    # If no valid token, show login/signup UI in the main column
    show_login_signup()


if __name__ == "__main__":
    main()
