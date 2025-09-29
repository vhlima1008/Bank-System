import streamlit as st
from shared.utils import guard_login, minimal_css

st.set_page_config(page_title="Balance", page_icon="💰", layout="centered")
minimal_css()
guard_login()

st.header("Balance")

def _try_call(obj, name):
    fn = getattr(obj, name, None)
    if callable(fn):
        try:
            return fn()
        except Exception:
            return None
    return None

def _try_attr(obj, *names):
    for n in names:
        if hasattr(obj, n):
            try:
                val = getattr(obj, n)
                if val is not None:
                    return val
            except Exception:
                pass
    return None

def get_current_balance():
    tx = st.session_state.get("tx")
    if not tx:
        return None, "no transaction in session"

    # 1) Transaction-level
    val = _try_attr(tx, "balance")
    if isinstance(val, (int, float)):
        return float(val), "tx.balance"

    val = _try_call(tx, "get_balance")
    if isinstance(val, (int, float)):
        return float(val), "tx.get_balance()"

    # 2) Client-level
    client = _try_attr(tx, "client")
    if client is not None:
        val = _try_attr(client, "balance", "current_balance", "account", "account_balance")
        if isinstance(val, (int, float)):
            return float(val), "client.attr"

        val = _try_call(client, "get_balance")
        if isinstance(val, (int, float)):
            return float(val), "client.get_balance()"

    return None, "not found"

balance, source = get_current_balance()

col1, col2 = st.columns([3, 1])
with col1:
    if balance is not None:
        # Display as a metric (no currency symbol to avoid assumptions)
        st.metric("Current Balance", f"R$ {balance:,.2f}")
    else:
        st.warning(
            "Balance not available. Ensure your domain exposes a balance field or method "
            "(e.g., `tx.balance`, `tx.get_balance()`, `tx.client.balance`, or `tx.client.get_balance()`)."
        )
with col2:
    st.caption(f"source: `{source}`")

st.markdown("---")
st.button("Refresh", on_click=lambda: None)
st.caption("See your balance evolution.")
