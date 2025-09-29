import io
import sys
import json
from datetime import datetime, date, time
from typing import Optional, Tuple

import streamlit as st

from shared.utils import guard_login, capture_print, minimal_css

st.set_page_config(page_title="Extract", page_icon="📄", layout="centered")
minimal_css()
guard_login()

# ---------------------- Helpers ----------------------

def _today_range() -> Tuple[datetime, datetime]:
    today = date.today()
    start = datetime.combine(today, time.min)
    end = datetime.combine(today, time.max)
    return start, end


def _call_extract_show_with_dates() -> str:
    """
    Try to call your domain extract with a date interval. We attempt common signatures
    in a best-effort manner to stay compatible with your domain code.
    Priority tries (in order):
      1) tx.extract.show(start_dt, end_dt)
      2) tx.extract.show(date_from=start_dt, date_to=end_dt)
      3) tx.extract.between(start_dt, end_dt)  # returns printable str or list/dict
      4) Fallback: tx.extract.show()  # no filtering supported
    Returns: printed output (string). If a method returns structured data, we render it below.
    """
    tx = st.session_state.tx
    start_dt: datetime = st.session_state.get("extract_start_dt")
    end_dt: datetime = st.session_state.get("extract_end_dt")

    printed = ""

    # 1) Positional show(start, end)
    try:
        buf = io.StringIO()
        with st.spinner("Loading extract..."):
            with st.redirect_stdout(buf):
                printed, _ret = capture_print(tx.extract.show, start_dt, end_dt)
        if printed:
            return printed
    except Exception:
        pass

    # 2) Keyword show(date_from=, date_to=)
    try:
        buf = io.StringIO()
        with st.spinner("Loading extract..."):
            with st.redirect_stdout(buf):
                printed, _ret = capture_print(tx.extract.show, date_from=start_dt, date_to=end_dt)
        if printed:
            return printed
    except Exception:
        pass

    # 3) A method that returns structured data
    try:
        between = getattr(tx.extract, "between", None)
        if callable(between):
            data = between(start_dt, end_dt)
            # Render structured data below (table/json) and also build a printable text
            _render_structured_extract(data)
            return _to_printable_text(data, start_dt, end_dt)
    except Exception:
        pass

    # 4) Fallback: no filtering supported
    try:
        printed, _ = capture_print(tx.extract.show)
    except Exception:
        printed = ""
    return printed or ""


def _render_structured_extract(data):
    """Best-effort renderer for dict/list/records."""
    try:
        import pandas as pd  # optional: used only if available
        if isinstance(data, list):
            if data and isinstance(data[0], dict):
                import pandas as pd
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                return
        if isinstance(data, dict):
            st.json(data)
            return
        # Fallback generic
        st.write(data)
    except Exception:
        st.write(data)


def _to_printable_text(data, start_dt: datetime, end_dt: datetime) -> str:
    header = f"Extract from {start_dt} to {end_dt}\n" + ("-" * 60) + "\n"
    try:
        if isinstance(data, list):
            if data and isinstance(data[0], dict):
                cols = list({k for row in data for k in row.keys()})
                lines = ["\t".join(cols)]
                for row in data:
                    lines.append("\t".join(str(row.get(c, "")) for c in cols))
                return header + "\n".join(lines)
            else:
                return header + "\n".join(str(x) for x in data)
        if isinstance(data, dict):
            return header + json.dumps(data, indent=2, ensure_ascii=False)
        return header + str(data)
    except Exception:
        return header + str(data)


def _printable_html_block(title: str, body_text: str) -> str:
    """Create a minimal print-friendly HTML (A4-ish) representation."""
    css = """
    <style>
      @page { size: A4; margin: 16mm; }
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: #222; }
      h1 { font-size: 20px; margin: 0 0 12px 0; }
      .meta { font-size: 12px; color: #666; margin-bottom: 12px; }
      pre { background: #f7f7f9; padding: 12px; border-radius: 8px; overflow-x: auto; }
      .footer { margin-top: 24px; font-size: 11px; color: #888; }
    </style>
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
    <!DOCTYPE html>
    <html><head><meta charset='utf-8'><title>{title}</title>{css}</head>
    <body>
      <h1>{title}</h1>
      <div class="meta">Generated at {now}</div>
      <pre>{body_text}</pre>
      <div class="footer">Bank-System • Streamlit export (print-friendly)</div>
    </body></html>
    """
    return html


# ---------------------- UI ----------------------

st.header("Extract")

# Date range filter (default: start/end of today)
start_default, end_default = _today_range()

with st.container():
    st.markdown("**Date interval** (defaults to today)")
    c1, c2, c3 = st.columns([1, 1, 0.4])
    with c1:
        start_d = st.date_input("Start date", value=start_default.date(), key="extract_start_date")
    with c2:
        end_d = st.date_input("End date", value=end_default.date(), key="extract_end_date")
    with c3:
        apply = st.button("Apply", type="primary")

# Persist selected datetimes in session (start of day → end of day)
if apply or "extract_start_dt" not in st.session_state:
    sdt = datetime.combine(st.session_state.get("extract_start_date", start_default.date()), time.min)
    edt = datetime.combine(st.session_state.get("extract_end_date", end_default.date()), time.max)
    # guard: ensure start <= end
    if sdt > edt:
        st.error("Start date must be before or equal to end date.")
        sdt, edt = start_default, end_default
    st.session_state.extract_start_dt = sdt
    st.session_state.extract_end_dt = edt

# Fetch and render extract for selected interval
printed = _call_extract_show_with_dates()

# Visual container card
st.markdown(
    """
    <div style="border:1px solid rgba(0,0,0,0.08); padding:16px; border-radius:12px; background:rgba(127,127,127,0.05)">
    <div style="font-size:13px; color:#666; margin-bottom:8px;">Printable output</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if printed.strip():
    st.code(printed, language="text")
else:
    st.info("No printable output from Extract for the selected interval. Showing a generic representation.")
    try:
        st.write(st.session_state.tx.extract)
    except Exception:
        st.warning("Unable to display extract. Ensure `extract.show()` prints output or expose a structured method like `between()`.")

# ---------------------- Download (Modal) ----------------------

DOWNLOAD_TITLE = "Download Extract (print-friendly)"
filename_hint = f"extract_{st.session_state.extract_start_dt.date()}_{st.session_state.extract_end_dt.date()}.html"
html_payload = _printable_html_block(
    title=f"Extract — {st.session_state.extract_start_dt} to {st.session_state.extract_end_dt}",
    body_text=printed.strip() or "(no printable output)",
)

# Prefer Streamlit dialog (1.32+). Fallback to expander if unavailable.
open_modal = st.button("Download as print…")

_dialog_supported = hasattr(st, "dialog") and callable(getattr(st, "dialog"))

if _dialog_supported:
    @st.dialog(DOWNLOAD_TITLE)
    def _download_dialog():
        st.write("Export a print-friendly HTML with your current extract interval.")
        st.download_button(
            label="Download HTML",
            data=html_payload.encode("utf-8"),
            file_name=filename_hint,
            mime="text/html",
            type="primary",
        )
        st.caption("You can open the HTML in your browser and use Ctrl/Cmd + P to print or save as PDF.")

    if open_modal:
        _download_dialog()
else:
    with st.expander(DOWNLOAD_TITLE, expanded=open_modal):
        st.download_button(
            label="Download HTML",
            data=html_payload.encode("utf-8"),
            file_name=filename_hint,
            mime="text/html",
            type="primary",
        )
        st.caption("Open the HTML and print/save as PDF.")

# Footer
st.markdown("---")
st.caption("Everything registred.")
