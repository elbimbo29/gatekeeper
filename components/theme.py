import streamlit as st
from auth.session_utils import cookies


def apply_theme(default="Dark"):
    # If a theme preference was saved in cookies, use it
    saved_theme = cookies.get("theme_choice") if cookies.ready() else None
    initial_index = 0 if (saved_theme or default) == "Dark" else 1

    # Sidebar toggle for Dark/Light mode
    theme_choice = st.sidebar.radio("🎨 Theme", ["Dark", "Light"], index=initial_index)

    # Save preference so it persists
    if cookies.ready():
        cookies["theme_choice"] = theme_choice

    # 👉 CSS overrides injected here
    # These <style> blocks are CSS rules applied to Streamlit’s internal HTML classes
    if theme_choice == "Dark":
        st.markdown(
            """
            <style>
            /* Dark theme CSS */
            .stApp { background-color: #0E1117; color: #FAFAFA; }
            .block-container { background-color: #0E1117; }
            .stSidebar { background-color: #262730; }
            .stButton>button { background-color: #4CAF50; color: white; }
            .stTextInput>div>input { background-color: #262730; color: #FAFAFA; }
            .stSelectbox>div>div>div { background-color: #262730; color: #FAFAFA; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            /* Light theme CSS */
            .stApp { background-color: #FFFFFF; color: #000000; }
            .block-container { background-color: #FFFFFF; color: #000000; }
            
            /* Sidebar background + text */
            .stSidebar { background-color: #F5F5F5; }
            .stSidebar, .stSidebar * { color: #000000 !important; }
            
            /* Input fields (username/password) */
            .stTextInput>div>input {
                background-color: #F5F5F5;
                color: #000000 !important;
            }
            
            /* Selectbox text */
            .stSelectbox>div>div>div {
                background-color: #F5F5F5;
                color: #000000 !important;
            }
            
            /* Buttons */
            .stButton>button {
                background-color: #1976D2;
                color: white;
                transition: background-color 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #1565C0; /* darker blue on hover */
            }

            /* Force labels and markdown text to black */
            label, .stMarkdown, h1, h2, h3, h4, h5, h6, p, span {
                color: #000000 !important;
            }

            /* Specifically fix Login/Signup radio options */
            .stRadio > label, .stRadio div, .stRadio span {
                color: #000000 !important;
            }

            /* Highlight selected option */
            .stRadio div[role="radiogroup"] label[data-baseweb="radio"] {
                background-color: #E3F2FD;
                border-radius: 5px;
                padding: 3px 6px;
            }

            /* Hover effect for Login/Signup options */
            .stRadio div[role="radiogroup"] label[data-baseweb="radio"]:hover {
                background-color: #BBDEFB;
                cursor: pointer;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
