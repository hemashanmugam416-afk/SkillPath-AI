


import streamlit as st
from google import genai
from supabase import create_client
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎓",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background-color: #F7F9FC;
    color: #1E293B;
}

h1, h2, h3 {
    color: #163A70 !important;
}

/* Name and degree boxes */
.stTextInput div[data-baseweb="input"] {
    background-color: #EAF3FF !important;
    border: 1px solid #B7D2F5 !important;
    border-radius: 10px !important;
}

.stTextInput input {
    background-color: #EAF3FF !important;
    color: #163A70 !important;
    -webkit-text-fill-color: #163A70 !important;
}

/* Role and level dropdowns */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #EAF3FF !important;
    border: 1px solid #B7D2F5 !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] span {
    color: #163A70 !important;
}

/* Skills multiselect */
.stMultiSelect div[data-baseweb="select"] > div {
    background-color: #EAF3FF !important;
    border: 1px solid #B7D2F5 !important;
    border-radius: 10px !important;
}

.stMultiSelect div[data-baseweb="tag"] {
    background-color: #D5E7FF !important;
}

/* Buttons */
div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #163A70 !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Sidebar and dividers */
section[data-testid="stSidebar"] {
    background-color: #EDF2FA;
}

hr {
    border-color: #D9E2F0;
}
</style>
""", unsafe_allow_html=True)

# ---------- Supabase authentication ----------
try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception:
    st.error("Supabase connection settings are missing. Check Streamlit Secrets.")
    st.stop()

if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

if not st.session_state.auth_user:
    st.title("🔐 Welcome to SkillPath AI")
    st.write("Create your own account or sign in to access your personal career workspace.")
    signup_tab, login_tab = st.tabs(["Create account", "Log in"])
