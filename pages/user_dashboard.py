"""
user_dashboard.py
-----------------
Streamlit User Dashboard:
- Displays personalized welcome
- Shows account info
- Provides user-only actions
"""

import streamlit as st


def user_dashboard(username: str):
    st.title("👤 User Dashboard")

    # Section 1: Welcome
    st.header("🎉 Welcome")
    st.success(f"Hello, {username}! You are logged in as a regular user.")

    # Section 2: Account Info
    st.header("📄 Account Information")
    st.write("Here you can view and update your account details.")
    st.info("Feature placeholder: profile editing, password change, etc.")

    # Section 3: User Actions
    st.header("⚡ User Actions")
    if st.button("View My Data"):
        st.write("Showing your personal data...")
    if st.button("Update Profile"):
        st.write("Redirecting to profile update flow...")
