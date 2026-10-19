


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
    with signup_tab:
        st.subheader("Create your account")

        signup_email = st.text_input(
            "Email address",
            key="signup_email"
        )
        signup_password = st.text_input(
            "Create password",
            type="password",
            key="signup_password"
        )
        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            key="confirm_password"
        )

        if st.button("Create account", key="signup_button"):
            if not signup_email.strip() or not signup_password:
                st.warning("Please enter your email and password.")
            elif len(signup_password) < 8:
                st.warning("Password must be at least 8 characters.")
            elif signup_password != confirm_password:
                st.warning("Passwords do not match.")
            else:
                try:
                    result = supabase.auth.sign_up({
                        "email": signup_email.strip(),
                        "password": signup_password
                    })
                    if result.user:
                        st.success(
                            "Account created! Check your email "
                            "if confirmation is required, then log in."
                        )
                    else:
                        st.info("Check your email to complete signup.")
                except Exception as e:
                    st.error(f"Signup failed: {e}")

    with login_tab:
        st.subheader("Welcome back")

        login_email = st.text_input(
            "Email address",
            key="login_email"
        )
        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Log in", key="login_button"):
            if not login_email.strip() or not login_password:
                st.warning("Please enter your email and password.")
            else:
                try:
                    result = supabase.auth.sign_in_with_password({
                        "email": login_email.strip(),
                        "password": login_password
                    })
                    st.session_state.auth_user = result.user
                    st.session_state.auth_session = result.session
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")

    st.stop()
