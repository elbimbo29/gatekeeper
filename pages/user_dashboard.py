import streamlit as st
from auth.check_auth import check_auth
from auth.session_utils import cookies, clear_token

st.set_page_config(page_title="User Dashboard", layout="wide")


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
    if st.sidebar.button("User Dashboard"):
        st.experimental_rerun()
    if st.sidebar.button("Admin Dashboard"):
        st.switch_page("pages/admin_dashboard.py")
        st.stop()
    if st.sidebar.button("Logs Dashboard"):
        st.switch_page("pages/logs_dashboard.py")
        st.stop()


def main():
    if not check_auth(required_role="user"):
        return

    render_sidebar_navigation()

    with st.container():
        st.markdown("## User Dashboard")
        st.markdown(
            f"**User:** {st.session_state.get('username', 'Unknown')} | **Role:** {st.session_state.get('role', 'unknown')}"
        )
        if st.button("Logout"):
            clear_session_and_redirect_to_login()

    st.write("User-specific content goes here.")
    st.markdown("---")
    st.write("Profile, settings, and user actions can be added here.")


if __name__ == "__main__":
    main()
