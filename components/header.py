import streamlit as st
from auth.session_utils import logout


def header_bar(username, role):
    # Top header bar with navigation
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

    with col1:
        st.markdown("## 🔐 Gatekeeper")

    with col2:
        st.markdown(f"**👤 User:** {username} | **Role:** {role}")

    with col3:
        st.markdown("### 🌐 Navigation")
        nav_choice = st.radio(
            "Go to:",
            ["Admin Dashboard", "User Dashboard", "Logs Dashboard"],
            horizontal=True,
            label_visibility="collapsed",
        )
        if nav_choice == "Admin Dashboard":
            st.switch_page("pages/admin_dashboard.py")
        elif nav_choice == "User Dashboard":
            st.switch_page("pages/user_dashboard.py")
        elif nav_choice == "Logs Dashboard":
            st.switch_page("pages/logs_dashboard.py")

    with col4:
        if st.button("🚪 Logout"):
            logout()
