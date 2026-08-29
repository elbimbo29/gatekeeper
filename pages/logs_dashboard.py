"""
logs_dashboard.py
-----------------
Admin-only dashboard to view, filter, search, and export logs inside Streamlit.
- Reads from gatekeeper.log
- Displays last N lines (default: 50)
- Provides filtering by log level (INFO, WARNING, ERROR)
- Allows keyword search (e.g., username, event type)
- Allows admins to download the full log file
"""

import streamlit as st
import os

LOG_FILE = "gatekeeper.log"


def logs_dashboard():
    st.header("📜 Logs Dashboard")

    if not os.path.exists(LOG_FILE):
        st.warning("No logs found yet.")
        return

    # Options for filtering
    level_filter = st.selectbox("Filter by level:", ["All", "INFO", "WARNING", "ERROR"])
    num_lines = st.slider("Number of lines to display:", 10, 200, 50)

    # Keyword search
    keyword = st.text_input("🔍 Search logs (e.g., username, event type)")

    # Read last N lines from log file
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()[-num_lines:]

    # Apply level filter
    if level_filter != "All":
        lines = [line for line in lines if f"- {level_filter} -" in line]

    # Apply keyword search
    if keyword:
        lines = [line for line in lines if keyword.lower() in line.lower()]

    # Display logs with icons
    for line in lines:
        if "INFO" in line:
            st.text(f"ℹ️ {line.strip()}")
        elif "WARNING" in line:
            st.text(f"⚠️ {line.strip()}")
        elif "ERROR" in line:
            st.text(f"🚨 {line.strip()}")
        else:
            st.text(line.strip())

    # --- Download button ---
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_data = f.read()
    st.download_button(
        label="⬇️ Download Full Log File",
        data=log_data,
        file_name="gatekeeper.log",
        mime="text/plain",
    )
