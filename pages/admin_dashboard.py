# pages/admin_dashboard.py
import streamlit as st
from datetime import datetime
from db.db_setup import SessionLocal
from db.models import User  # keep User import

# Try to import LogEntry if it exists; otherwise fall back to None
try:
    from db.models import LogEntry
except Exception:
    LogEntry = None

from auth.check_auth import check_auth
from auth.session_utils import cookies, clear_token
from auth.auth_utils import hash_password

st.set_page_config(page_title="Admin Dashboard", layout="wide")

PAGE_TITLE = "Admin Dashboard"


def fetch_users(limit=500):
    db = SessionLocal()
    try:
        return db.query(User).order_by(User.id.desc()).limit(limit).all()
    finally:
        db.close()


def create_user(username, password, role="user"):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            return False, "Username already exists"
        new_user = User(
            username=username, password_hash=hash_password(password), role=role
        )
        db.add(new_user)
        db.commit()
        return True, "User created"
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()


def fetch_recent_logs(limit=200):
    """
    If LogEntry model is available, query it.
    If not, return an empty list so the page does not crash.
    """
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


def render_header(username, role):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## {PAGE_TITLE}")
        st.markdown(f"**User:** {username}  |  **Role:** {role}")
    with col2:
        if st.button("Logout"):
            clear_session_and_redirect_to_login()


def render_sidebar_navigation():
    st.sidebar.markdown("### Navigation")
    if st.sidebar.button("Admin Dashboard"):
        st.experimental_rerun()
    if st.sidebar.button("User Dashboard"):
        st.switch_page("pages/user_dashboard.py")
        st.stop()
    if st.sidebar.button("Logs Dashboard"):
        st.switch_page("pages/logs_dashboard.py")
        st.stop()
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Admin Actions")
    if st.sidebar.button("Create Test User"):
        ok, msg = create_user("test_user_auto", "password123", role="user")
        if ok:
            st.sidebar.success("Test user created")
        else:
            st.sidebar.error(msg)


def render_metrics():
    with st.container():
        st.subheader("Overview Metrics")
        col1, col2, col3 = st.columns(3)
        users_count = 0
        try:
            db = SessionLocal()
            users_count = db.query(User).count()
        except Exception:
            users_count = 0
        finally:
            try:
                db.close()
            except Exception:
                pass
        col1.metric("Total Users", users_count)
        col2.metric("Active Sessions", "—")
        # If LogEntry not available show N/A
        col3.metric("Recent Logs", "N/A" if LogEntry is None else "—")


def render_user_table():
    st.subheader("User Management")
    users = fetch_users(limit=500)
    if not users:
        st.info("No users found")
        return
    rows = []
    for u in users:
        rows.append({"id": u.id, "username": u.username, "role": u.role})
    st.table(rows)

    st.markdown("#### Create New User")
    with st.form("create_user_form", clear_on_submit=True):
        cu_col1, cu_col2, cu_col3 = st.columns([2, 2, 1])
        with cu_col1:
            new_username = st.text_input("Username", key="new_user_username")
        with cu_col2:
            new_password = st.text_input(
                "Password", type="password", key="new_user_password"
            )
        with cu_col3:
            new_role = st.selectbox(
                "Role", ["user", "admin", "logs"], key="new_user_role"
            )
        submitted = st.form_submit_button("Create User")
        if submitted:
            if not new_username or not new_password:
                st.error("Username and password required")
            else:
                ok, msg = create_user(new_username.strip(), new_password, role=new_role)
                if ok:
                    st.success("User created successfully")
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to create user: {msg}")


def render_logs_viewer():
    st.subheader("Recent Logs")
    if LogEntry is None:
        st.info("Log model not available. No logs to show.")
        return
    try:
        logs = fetch_recent_logs(limit=200)
    except Exception:
        logs = []
    if not logs:
        st.info("No logs available")
        return
    for entry in logs[:200]:
        ts = getattr(entry, "timestamp", None)
        msg = getattr(entry, "message", str(entry))
        ts_str = (
            ts.strftime("%Y-%m-%d %H:%M:%S") if isinstance(ts, datetime) else str(ts)
        )
        st.markdown(f"- **{ts_str}**  {msg}")


def main():
    # Auth guard
    if not check_auth(required_role="admin"):
        return

    username = st.session_state.get("username", "Unknown")
    role = st.session_state.get("role", "unknown")

    render_sidebar_navigation()
    render_header(username, role)

    with st.container():
        render_metrics()
        st.markdown("---")
        left, right = st.columns([2, 1])
        with left:
            render_user_table()
        with right:
            render_logs_viewer()

    st.markdown("---")
    st.caption("Admin tools — use with care")


if __name__ == "__main__":
    main()
