import streamlit as st
from auth.check_auth import check_auth
from auth.session_utils import clear_token
from db.db_setup import SessionLocal

# Defensive import: LogEntry may not exist in db.models
try:
    from db.models import LogEntry
except Exception:
    LogEntry = None

st.set_page_config(page_title="Logs Dashboard", layout="wide")


def fetch_logs(limit=500):
    if LogEntry is None:
        return []
    db = SessionLocal()
    try:
        return db.query(LogEntry).order_by(LogEntry.timestamp.desc()).limit(limit).all()
    finally:
        db.close()


def clear_session_and_redirect_to_login():
    try:
        clear_token()
    except Exception:
        pass
    st.success("Logged out")
    st.switch_page("pages/login.py")
    st.stop()


def render_sidebar_navigation():
    st.sidebar.markdown("### Navigation")
    if st.sidebar.button("Logs Dashboard"):
        st.experimental_rerun()
    if st.sidebar.button("User Dashboard"):
        st.switch_page("pages/user_dashboard.py")
        st.stop()
    if st.sidebar.button("Admin Dashboard"):
        st.switch_page("pages/admin_dashboard.py")
        st.stop()


def main():
    # Allow logs users and admins (admin is allowed by check_auth)
    if not check_auth(required_roles=["logs", "user"]):
        return

    render_sidebar_navigation()

    with st.container():
        st.markdown("## Logs Dashboard")
        st.markdown(
            f"**User:** {st.session_state.get('username', 'Unknown')} | **Role:** {st.session_state.get('role', 'unknown')}"
        )
        if st.button("Logout"):
            clear_session_and_redirect_to_login()

    logs = []
    try:
        logs = fetch_logs(limit=500)
    except Exception:
        logs = []

    if LogEntry is None:
        st.info("Log model not available. No logs to show.")
        return

    if not logs:
        st.info("No logs available")
        return

    st.subheader("Recent Logs")
    for entry in logs[:200]:
        ts = getattr(entry, "timestamp", None)
        msg = getattr(entry, "message", str(entry))
        ts_str = (
            ts.strftime("%Y-%m-%d %H:%M:%S") if hasattr(ts, "strftime") else str(ts)
        )
        st.markdown(f"- **{ts_str}**  {msg}")


if __name__ == "__main__":
    main()
