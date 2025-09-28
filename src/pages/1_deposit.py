# pages/1_Deposit.py
import streamlit as st
from shared.utils import guard_login, minimal_css

st.set_page_config(page_title="Deposit", page_icon="➕", layout="centered")
minimal_css()
guard_login()

st.header("Deposit")
with st.form("deposit_form"):
    amount = st.number_input("Amount", min_value=0.0, step=10.0, format="%.2f")
    submit = st.form_submit_button("Confirm deposit")

if submit:
    if amount <= 0:
        st.error("Amount must be greater than 0.")
    else:
        try:
            st.session_state.tx.execute("deposit", float(amount))
            st.success(f"Deposit of {amount:.2f} completed.")
        except Exception as e:
            st.error(f"Deposit failed: {e}")

st.markdown("---")
st.caption("Deposit • Minimal and clean form")
