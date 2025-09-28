# Bank-System

![Languages](https://img.shields.io/github/languages/count/vhlima1008/Bank-System)
![Activity](https://img.shields.io/github/commit-activity/t/vhlima1008/Bank-System)
![Contributors](https://img.shields.io/github/contributors/vhlima1008/Bank-System)
![Size](https://img.shields.io/github/repo-size/vhlima1008/Bank-System)

<!-- Optional:
![Last commit](https://img.shields.io/github/last-commit/vhlima1008/Bank-System)
![Issues](https://img.shields.io/github/issues/vhlima1008/Bank-System)
-->

> Educational “Digital Bank” prototype in **Python** with a **minimalist Streamlit UI**. Includes **login**, **balance**, **deposits/withdrawals**, **PRICE financing + CET**, and **statement** (printed output captured in the UI).

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Architecture](#architecture)
* [Project Structure](#project-structure)
* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Run](#run)
* [Using the App](#using-the-app)
* [Pages (Multipage UI)](#pages-multipage-ui)
* [Configuration](#configuration)
* [Troubleshooting](#troubleshooting)
* [Roadmap](#roadmap)
* [Good Practices Adopted](#good-practices-adopted)
* [Disclaimer](#disclaimer)
* [License](#license)
* [Contributing](#contributing)

---

## Overview

**Bank-System** demonstrates a simple, layered architecture for core banking operations, separating **domain logic** (`User`, `Transaction`, `Extract`, `Financing`) from the **presentation layer** (Streamlit). It’s designed as a clean starting point for learning **good structure**, **layered design**, and **rapid prototyping** with Python.

**Key idea:** keep your **business logic** pure and framework-agnostic in the `app/core` package; let Streamlit only **consume** it for UI and state handling.

---

## Features

* **Login (mock)** with session stored in `st.session_state`.
* **Balance** page for the current account balance.
* **Deposit** and **Withdraw** operations with input validation and clear error messages.
* **Financing** simulation using **PRICE** amortization and **CET** (Effective Total Cost).

  * Compatible with domain code that **prints** a full amortization table; the UI captures and displays it.
* **Statement** that renders whatever your domain prints via `extract.show()`.
* **Minimalist UI**: clean layout, concise feedback (`success`/`error`), modular pages.
* **Modular architecture**: domain in `app/core`, UI entry in `app.py`, pages in `pages/`, helpers in `shared/`.

---

## Architecture

**Simplified flow**

1. **Home** (`app.py`) authenticates the user (mock), creates `User` and `Transaction`, and stores them in `st.session_state`.
2. Pages read `st.session_state.tx` and call `execute("deposit"|"withdraw"|"financing", ...)`.
3. **Statement/Financing**: if the domain prints tables (e.g., with `print()` inside `extract.show()` or `execute("financing", ...)`), the UI captures `stdout` and displays it.

---

## Project Structure

```txt
/ (repo root)
├─ app/
│  └─ core/               # Domain logic (no UI code)
│     ├─ user.py          # User entity and related logic
│     ├─ transaction.py   # Orchestrates deposits, withdrawals, financing, extract
│     ├─ extract.py       # Statement utilities and display helpers
│     └─ financing.py     # PRICE schedule, CET, interest/fees
├─ shared/
│  └─ utils.py            # Shared helpers: print capture, login guard, minimal CSS
├─ app.py                 # Home (login/logout) + session bootstrap
└─ pages/                 # Streamlit multipage UI
   ├─ 0_Balance.py        # Current balance
   ├─ 1_Deposit.py        # Deposit form & validation
   ├─ 2_Withdraw.py       # Withdraw form & validation
   ├─ 3_Financing.py      # Financing simulation (prints + return)
   └─ 4_Extract.py        # Statement (captures extract.show() prints)
```

---

## Getting Started

### Prerequisites

* **Python 3.10+**
* **pip** (or **uv/pipx**)

### Installation

```bash
# 1) Clone
git clone https://github.com/vhlima1008/Bank-System
cd Bank-System

# 2) (Optional) Virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Dependencies
pip install -r requirements.txt
# If requirements.txt is not present yet:
pip install streamlit
```

### Run

```bash
# From the repo root (where the "app/" package lives):
streamlit run app.py

# If you see import issues, try:
python -m streamlit run app.py
```

> Tip: If your IDE/runner changes the working directory, ensure the **project root** is used so `from app.core...` resolves correctly.

---

## Using the App

1. Open **Home** → enter **Name/Email/Age** → **Login**.
2. Use the sidebar to navigate through the pages:

   * **Balance** → current balance metric.
   * **Deposit** / **Withdraw** → operations with validation and instant feedback.
   * **Financing** → simulate PRICE installments; shows CET and any printed amortization table.
   * **Extract** → prints whatever your domain’s `extract.show()` outputs.

---

## Pages (Multipage UI)

* **Home (`app.py`)**

  * Mock login (no real auth provider).
  * Initializes `User` and `Transaction` and stores them in the session.

* **0_Balance.py**

  * Shows the current balance.
  * Tries common attribute/method names (e.g., `tx.balance`, `tx.get_balance()`, `tx.client.balance`) for compatibility.

* **1_Deposit.py / 2_Withdraw.py**

  * Simple forms with validation: amounts must be `> 0`.
  * Calls `st.session_state.tx.execute("deposit"|"withdraw", amount)`.

* **3_Financing.py**

  * Inputs: `principal` and `months`.
  * Captures any **printed output** (e.g., a PRICE table) from `execute("financing", ...)`.
  * Displays both the **printed table** (if any) and the **return value** (dict/list/string/object).

* **4_Extract.py**

  * Captures printed output from `st.session_state.tx.extract.show()`.
  * Falls back to `st.write(tx.extract)` if nothing is printed.

---

## Configuration

* **Minimal CSS**: `shared/utils.py` includes a tiny CSS to hide Streamlit’s default menu/footer and keep spacing tight.
* **Session**: relies on `st.session_state` keys: `logged`, `user`, and `tx`.
* **Domain compatibility**: the UI assumes:

  * `Transaction.execute(kind, ...)` exists for `"deposit"`, `"withdraw"`, and `"financing"`.
  * `tx.extract.show()` prints a statement table (or similar). If not, the UI will fall back to a generic view.

---

## Troubleshooting

* **`ModuleNotFoundError: app.core...`**

  * Run from the **project root**, not from inside `app/`.
  * Try `python -m streamlit run app.py`.
  * As a last resort, add a `sys.path.append(str(ROOT))` tweak at the top of files (commented in code).

* **Nothing appears in Statement/Financing tables**

  * Ensure your domain actually **prints** inside `extract.show()` or during `execute("financing", ...)`.
  * The UI already captures `stdout` and renders it as a code block.

* **Amounts not accepted**

  * Inputs must be **greater than zero**. Validation errors are shown via `st.error`.

* **Wide layout**

  * Change `st.set_page_config(..., layout="centered")` to `"wide"` if needed.

---

## Roadmap

* [ ] DataFrame-based **statement** with filters (`st.dataframe`).
* [ ] **SQLite** persistence (tables: `users`, `transactions`).
* [ ] Real authentication (e.g., `streamlit-authenticator` or a simple REST backend).
* [ ] Unit tests for domain logic (`pytest`).
* [ ] Theming (colors/typography) and **i18n**.

---

## Good Practices Adopted

* **Layered separation**: domain vs. UI.
* **Input validation** with succinct user feedback.
* **Print capture** to support domain code that prints reports/tables.
* **Modular pages** for readability and maintenance.

---

## Disclaimer

This repository is **educational/prototypal**. It is not production-ready and does not handle real banking requirements such as compliance, security, privacy (LGPD/GDPR), antifraud, etc.

---

## License

Choose a license (e.g., **MIT**). If you prefer, add a `LICENSE` file and update this section accordingly.

---

## Contributing

Contributions and suggestions are welcome!
Please open an **issue** describing the context and your proposed change, or submit a **pull request**.
