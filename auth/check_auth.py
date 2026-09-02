import streamlit as st
from auth.session_utils import cookies, decode_jwt


def check_auth(required_role=None, required_roles=None):
    """
    Backwards-compatible auth check.
    Accepts either `required_role` (str) or `required_roles` (str or iterable).
    Admins are treated as superusers and are allowed everywhere.
    On failure, redirects to pages/login.py and stops execution.
    """
    try:
        if not cookies.ready():
            _redirect_to_login("Cookies not ready. Please login.")
            return False
    except Exception:
        _redirect_to_login("Cookie access error. Please login.")
        return False

    token = cookies.get("jwt_token")
    if not token:
        _redirect_to_login("No session token found. Please login.")
        return False

    try:
        payload = decode_jwt(token)
    except Exception:
        payload = None

    if not payload:
        _redirect_to_login("Invalid or expired session. Please login.")
        return False

    st.session_state["logged_in"] = True
    st.session_state["username"] = payload.get("username")
    st.session_state["role"] = payload.get("role")

    # Normalize inputs to a set of allowed roles
    allowed = None
    if required_role is not None:
        allowed = {required_role}
    elif required_roles is not None:
        if isinstance(required_roles, str):
            allowed = {required_roles}
        else:
            try:
                allowed = set(required_roles)
            except Exception:
                allowed = set(required_roles or [])

    # Admin is superuser: always allow
    current_role = st.session_state.get("role")
    if current_role == "admin":
        return True

    # If roles were specified, enforce them
    if allowed is not None and current_role not in allowed:
        _redirect_to_login(
            f"Unauthorized. Required role(s): {', '.join(sorted(allowed))}"
        )
        return False

    return True


def _redirect_to_login(message="Please login again."):
    st.error(message)
    st.switch_page("pages/login.py")
    st.stop()
