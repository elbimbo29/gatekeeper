# auth/session_utils.py

import os
import jwt
import datetime
import logging
import streamlit as st
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager

# --- Load secrets ---
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
COOKIE_PASSWORD = os.getenv("COOKIE_PASSWORD")

# --- Cookie Manager (single instance for the whole app) ---
cookies = EncryptedCookieManager(prefix="gatekeeper", password=COOKIE_PASSWORD)

# If cookies manager isn't ready, stop execution until it is.
if not cookies.ready():
    st.stop()


def decode_jwt(token: str):
    """
    Decode a JWT token and return the payload dict, or None on failure/expiry.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None


def create_jwt(payload: dict) -> str:
    """
    Create a JWT token from payload.
    """
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def clear_token():
    """
    Clear the stored JWT token (cookie) and remove auth keys from session_state.
    Safe no-op if cookies object or keys are missing.
    """
    try:
        if "jwt_token" in cookies:
            cookies["jwt_token"] = ""
        if "role" in cookies:
            cookies["role"] = ""
        try:
            cookies.save()
        except Exception:
            # best-effort: ignore cookie save failures
            logging.exception("Failed to save cookies while clearing token.")
    except Exception:
        # If cookies isn't defined or another error occurs, ignore and continue
        logging.exception("Error while clearing cookies.")

    # Clear session state keys used for auth
    for key in ("logged_in", "username", "role"):
        try:
            st.session_state.pop(key, None)
        except Exception:
            pass


def logout():
    """
    Log the user out: clear cookies, inform user, and redirect to login page.
    """
    try:
        if "jwt_token" in cookies:
            cookies["jwt_token"] = ""
        if "role" in cookies:
            cookies["role"] = ""
        try:
            cookies.save()
        except Exception:
            logging.exception("Failed to save cookies during logout.")
    except Exception:
        logging.exception("Error while clearing cookies during logout.")

    # Clear session state
    for key in ("logged_in", "username", "role"):
        try:
            st.session_state.pop(key, None)
        except Exception:
            pass

    st.info("👋 You have been logged out.")
    logging.info("User logged out.")
    # Use the file path for switch_page and stop execution immediately after redirect
    st.switch_page("pages/login.py")
    st.stop()


def refresh_session(payload: dict):
    """
    Refresh the session expiry in the provided payload and persist a new token.
    """
    try:
        new_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            hours=1
        )
        payload["exp"] = int(new_expiry.timestamp())
        new_token = create_jwt(payload)
        cookies["jwt_token"] = new_token
        try:
            cookies.save()
        except Exception:
            logging.exception("Failed to save cookies when refreshing session.")
        st.success("🔄 Session refreshed for another hour!")
        logging.info(f"User {payload.get('username')} refreshed their session.")
        st.experimental_rerun()
    except Exception:
        logging.exception("Failed to refresh session.")
        st.error("Could not refresh session.")


def check_session(required_role: str = None):
    """
    Validate the current session and optional role requirement.
    Returns the payload dict on success, or None on failure (and redirects to login).
    """
    if not cookies.ready():
        st.stop()

    token = cookies.get("jwt_token")
    payload = decode_jwt(token) if token else None

    if not payload:
        st.error("❌ You must be logged in to view this page.")
        logout()
        return None

    # Validate expiry using timezone-aware timestamps
    try:
        expiry_time = datetime.datetime.fromtimestamp(
            payload["exp"], tz=datetime.timezone.utc
        )
        remaining = expiry_time - datetime.datetime.now(datetime.timezone.utc)
    except Exception:
        # If payload doesn't contain exp or timestamp parsing fails, force logout
        st.error("❌ Invalid session data. Please log in again.")
        logout()
        return None

    if remaining.total_seconds() <= 0:
        st.error("⏳ Session expired. Please log in again.")
        logout()
        return None

    if required_role and payload.get("role") != required_role:
        st.error(f"❌ Unauthorized. You need role: {required_role}")
        logout()
        return None

    return payload
