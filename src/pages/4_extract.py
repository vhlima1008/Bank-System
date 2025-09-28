# pages/4_Extract.py
import streamlit as st
from shared.utils import guard_login, capture_print, minimal_css

st.set_page_config(page_title="Extract", page_icon="📄", layout="centered")
minimal_css()
guard_login()

st.header("Extract")

# Prefer printing output from your domain object's extract.show()
try:
    printed, _ = capture_print(st.session_state.tx.extract.show)
except Exception:
    printed = ""

if printed.strip():
    st.code(printed, language="text")
else:
    st.info("No printable output from Extract. Showing a generic representation.")
    try:
        st.write(st.session_state.tx.extract)
    except Exception:
        st.warning("Unable to display extract. Ensure `extract.show()` prints output.")

st.button("Refresh", on_click=lambda: None)
st.markdown("---")
st.caption("Extract • Displays printed output from your domain code when available")
