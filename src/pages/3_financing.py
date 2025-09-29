import streamlit as st
from shared.utils import guard_login, capture_print, minimal_css

st.set_page_config(page_title="Financing", page_icon="💠", layout="centered")
minimal_css()
guard_login()

st.header("Financing")
with st.form("financing_form"):
    principal = st.number_input("Principal", min_value=0.0, step=100.0, format="%.2f")
    months = st.number_input("Months", min_value=0, step=1, format="%d")
    submit = st.form_submit_button("Simulate financing")

if submit:
    # alerts for wrong inputs
    if principal <= 0:
        st.error("Principal must be greater than 0.")
    elif months <= 0:
        st.error("Number of months must be greater than 0.")
    else:
        try:
            # capture any printed financing table produced by your domain code
            printed, result = capture_print(st.session_state.tx.execute, "financing", float(principal), int(months))

            if printed.strip():
                st.subheader("Financing Table (printed by your domain code)")
                st.code(printed, language="text")

            st.subheader("Financing Result (return value)")
            if result is None:
                st.info("No result returned by execute('financing', ...).")
            elif isinstance(result, dict):
                st.write(result)
            elif isinstance(result, (list, tuple)):
                st.table(result)
            elif isinstance(result, str):
                st.code(result, language="text")
            else:
                st.write(result)

            st.success("Financing simulation completed.")
        except Exception as e:
            st.error(f"Financing execution failed: {e}")

st.markdown("---")
st.caption("Simulate your future financing.")
