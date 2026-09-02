import streamlit as st
from db.db_setup import SessionLocal
from db.models import User
from auth.auth_utils import hash_password, verify_password


def change_password(username: str):
    st.subheader("🔒 Change Password")

    old_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("✅ Update Password"):
        if new_password != confirm_password:
            st.error("❌ New passwords do not match.")
            return

        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        if not user:
            st.error("❌ User not found.")
            db.close()
            return

        if not verify_password(old_password, user.password_hash):
            st.error("❌ Current password is incorrect.")
            db.close()
            return

        user.password_hash = hash_password(new_password)
        db.commit()
        db.close()
        st.success("✅ Password updated successfully!")
