import streamlit as st
from shared.utils import guard_login, minimal_css

st.set_page_config(page_title="Withdraw", page_icon="➖", layout="centered")
minimal_css()
guard_login()

st.header("Withdraw")
with st.form("withdraw_form"):
    amount = st.number_input("Amount", min_value=0.0, step=10.0, format="%.2f")
    submit = st.form_submit_button("Confirm withdraw")

if submit:
    if amount <= 0:
        st.error("Amount must be greater than 0.")
    else:
        try:
            st.session_state.tx.execute("withdraw", float(amount))
            st.success(f"Withdraw of {amount:.2f} completed.")
        except Exception as e:
            st.error(f"Withdraw failed: {e}")

st.markdown("---")
st.caption("Withdraw for a good reason.")
