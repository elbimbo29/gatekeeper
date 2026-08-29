"""
admin_dashboard.py
------------------
Streamlit Admin Dashboard:
- Displays user management tools
- Shows system stats
- Provides admin-only actions
"""

import streamlit as st
from db.db_setup import SessionLocal
from db.models import User
from pages.logs_dashboard import logs_dashboard


def admin_dashboard():
    st.title("🔐 Admin Dashboard")

    # Admin-only tools section
    st.subheader("Admin Tools")
    logs_dashboard()  # ✅ integrate logs viewer

    # Section 1: User Management
    st.header("👥 User Management")
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    for user in users:
        st.write(f"- {user.username} ({user.role})")

    # Section 2: System Stats
    st.header("📊 System Stats")
    st.metric("Total Users", len(users))
    st.metric("Admins", len([u for u in users if u.role == "admin"]))
    st.metric("Regular Users", len([u for u in users if u.role == "user"]))

    # Section 3: Admin Actions
    st.header("⚙️ Admin Actions")
    if st.button("Create New User"):
        st.info("Redirect to signup flow...")
    if st.button("Delete User"):
        st.warning("Redirect to delete flow...")
