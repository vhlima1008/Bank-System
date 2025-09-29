import io
import sys
from pathlib import Path
import streamlit as st

from app.core.transaction import Transaction
from app.core.user import User

st.set_page_config(page_title="Digital Bank", page_icon="💳", layout="centered")
st.markdown("""
<style>
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

def ensure_session():
    if "logged" not in st.session_state:
        st.session_state.logged = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "tx" not in st.session_state:
        st.session_state.tx = None

def make_user_and_tx(name: str, email: str, age: int):
    user = User(name, email, age)
    tx = Transaction(user)
    return user, tx

ensure_session()

st.title("Digital Bank")
st.caption("Minimal for make more.")

if not st.session_state.logged:
    st.header("Login")
    with st.form("login_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", value="Victor")
            age_str = st.text_input("Age", value="19")
        with col2:
            email = st.text_input("Email", value="victor@email.com")
            password = st.text_input("Password", type="password", value="123456")  # mock-only
        submitted = st.form_submit_button("Login")

        if submitted:
            errors = []
            if not name.strip():
                errors.append("Name is required.")
            if not email.strip() or "@" not in email:
                errors.append("Valid email is required.")
            try:
                age = int(age_str)
                if age <= 0:
                    errors.append("Age must be greater than 0.")
            except ValueError:
                errors.append("Age must be a valid integer.")

            if errors:
                for e in errors: st.error(e)
            else:
                try:
                    user, tx = make_user_and_tx(name.strip(), email.strip(), int(age))
                    st.session_state.user = user
                    st.session_state.tx = tx
                    st.session_state.logged = True
                    st.success("Logged in successfully. Use the sidebar to navigate: Deposit, Withdraw, Financing, Extract.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")
else:
    st.success(f"Welcome, {getattr(st.session_state.user, 'name', 'User')}! Use the sidebar pages.")
    if st.button("Logout"):
        for k in ["logged", "user", "tx"]:
            st.session_state.pop(k, None)
        st.success("You have been logged out.")
        st.rerun()

st.markdown("---")
st.caption("For start your jouney, use the sidebar.")
