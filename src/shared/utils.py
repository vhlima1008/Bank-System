import io
import contextlib
import streamlit as st

def guard_login():
    if not st.session_state.get("logged"):
        st.warning("You need to be logged in. Go to the Home page to login.")
        st.stop()

def capture_print(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = fn(*args, **kwargs)
    return buf.getvalue(), result

def minimal_css():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    </style>
    """, unsafe_allow_html=True)
