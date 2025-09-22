from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation, getcontext
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import hashlib
import pandas as pd
import customtkinter as ctk
from typing import Optional

getcontext().prec = 28  # precisão adequada para dinheiro

DATA_DIR = Path("src/users")
USERS_CSV = DATA_DIR / "users.csv"
TX_CSV = DATA_DIR / "transactions.csv"
DATE_FMT = "%Y-%m-%d %H:%M:%S"

# ===================== Persistência (Pandas) =====================

class Storage:
    def __init__(self, users_csv: Path = USERS_CSV, tx_csv: Path = TX_CSV):
        self.users_csv = users_csv
        self.tx_csv = tx_csv
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Inicializa arquivos se não existirem
        if not self.users_csv.exists():
            pd.DataFrame(columns=[
                "user_id","username","email","age","password_hash",
                "created_at","last_login_at","last_logout_at","balance"
            ]).to_csv(self.users_csv, index=False)

        if not self.tx_csv.exists():
            pd.DataFrame(columns=[
                "tx_id","user_id","kind","amount","timestamp","note","balance_after"
            ]).to_csv(self.tx_csv, index=False)

    # ---- Users ----
    def _read_users(self) -> pd.DataFrame:
        df = pd.read_csv(self.users_csv, dtype=str).fillna("")
        # normaliza tipos básicos
        if not df.empty:
            if "age" in df.columns:
                df["age"] = df["age"].apply(lambda x: int(x) if str(x).isdigit() else 0)
        return df

    def _write_users(self, df: pd.DataFrame) -> None:
        df.to_csv(self.users_csv, index=False)

    def _read_tx(self) -> pd.DataFrame:
        return pd.read_csv(self.tx_csv, dtype=str).fillna("")

    def _write_tx(self, df: pd.DataFrame) -> None:
        df.to_csv(self.tx_csv, index=False)

    def get_user_by_username(self, username: str) -> Optional[dict]:
        df = self._read_users()
        if df.empty:
            return None
        m = df["username"].str.lower() == username.lower()
        if not m.any():
            return None
        row = df[m].iloc[0].to_dict()
        # normaliza balance para Decimal
        row["balance"] = Decimal(row.get("balance") or "0.00")
        return row

    def _next_user_id(self) -> str:
        df = self._read_users()
        if df.empty:
            return "1"
        return str(df["user_id"].astype(int).max() + 1)

    def create_user(self, username: str, email: str, age: int, password_hash: str) -> dict:
        if self.get_user_by_username(username):
            raise ValueError("Usuário já existe.")

        user_id = self._next_user_id()
        now = datetime.now().strftime(DATE_FMT)
        new_row = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "age": age,
            "password_hash": password_hash,
            "created_at": now,
            "last_login_at": "",
            "last_logout_at": "",
            "balance": "0.00",
        }
        df = self._read_users()
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self._write_users(df)
        # retorna já tipado
        new_row["balance"] = Decimal("0.00")
        return new_row

    def set_login_time(self, user_id: str) -> None:
        df = self._read_users()
        if df.empty:
            return
        now = datetime.now().strftime(DATE_FMT)
        df.loc[df["user_id"] == str(user_id), "last_login_at"] = now
        self._write_users(df)

    def set_logout_time(self, user_id: str) -> None:
        df = self._read_users()
        if df.empty:
            return
        now = datetime.now().strftime(DATE_FMT)
        df.loc[df["user_id"] == str(user_id), "last_logout_at"] = now
        self._write_users(df)

    def update_user_balance(self, user_id: str, new_balance: Decimal) -> None:
        df = self._read_users()
        df.loc[df["user_id"] == str(user_id), "balance"] = f"{new_balance:.2f}"
        self._write_users(df)

    # ---- Transactions ----
    def _next_tx_id(self) -> str:
        df = self._read_tx()
        if df.empty:
            return "1"
        return str(df["tx_id"].astype(int).max() + 1)

    def append_transaction(
        self,
        user_id: str,
        kind: str,           # "DEPOSIT" | "WITHDRAW"
        amount: Decimal,
        note: str,
        balance_after: Decimal
    ) -> None:
        df = self._read_tx()
        tx_id = self._next_tx_id()
        row = {
            "tx_id": tx_id,
            "user_id": str(user_id),
            "kind": kind,
            "amount": f"{amount:.2f}",
            "timestamp": datetime.now().strftime(DATE_FMT),
            "note": note or "",
            "balance_after": f"{balance_after:.2f}",
        }
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        self._write_tx(df)

    def get_transactions(self, user_id: str) -> pd.DataFrame:
        df = self._read_tx()
        if df.empty:
            return df
        return df[df["user_id"] == str(user_id)].copy()

# ===================== Domínio =====================

@dataclass
class Transaction:
    kind: str         # "DEPOSIT" | "WITHDRAW"
    amount: Decimal
    timestamp: datetime
    note: str = ""

class Client:
    def __init__(self, user_row: dict, storage: Storage):
        self.user_id = str(user_row["user_id"])
        self.name = user_row["username"]
        self.email = user_row["email"]
        self.age = int(user_row["age"])
        self._balance = Decimal(user_row.get("balance", Decimal("0.00")))
        self.storage = storage

    @property
    def balance(self) -> Decimal:
        return self._balance

    def _quantize(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def deposit(self, value: Decimal, note: str = ""):
        value = self._quantize(value)
        if value <= 0:
            raise ValueError("Valor do depósito deve ser positivo.")
        self._balance = self._quantize(self._balance + value)
        # persiste
        self.storage.update_user_balance(self.user_id, self._balance)
        self.storage.append_transaction(self.user_id, "DEPOSIT", value, note, self._balance)

    def withdraw(self, value: Decimal, note: str = ""):
        value = self._quantize(value)
        if value <= 0:
            raise ValueError("Valor do saque deve ser positivo.")
        if self._balance - value < 0:
            raise ValueError("Saldo insuficiente para saque.")
        self._balance = self._quantize(self._balance - value)
        # persiste
        self.storage.update_user_balance(self.user_id, self._balance)
        self.storage.append_transaction(self.user_id, "WITHDRAW", value, note, self._balance)

# ===================== UI / App =====================

def br_money(d: Decimal) -> str:
    """Formata Decimal para 'R$ 1.234,56'."""
    s = f"{d:,.2f}"
    return "R$ " + s.replace(",", "X").replace(".", ",").replace("X", ".")

def parse_amount_str(raw: str) -> Decimal:
    raw = (raw or "").replace(",", ".").strip()
    return Decimal(raw)

def hash_password(p: str) -> str:
    # Demonstração: hash simples (não usar em produção)
    return hashlib.sha256((p or "").encode()).hexdigest()

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Bank System")
        self.geometry("620x480")

        # Persistência
        self.storage = Storage()

        # Estado
        self.current_client: Optional[Client] = None

        # Vars compartilhadas
        self.usernameVar = ctk.StringVar()
        self.passwordVar = ctk.StringVar()
        self.amountVar   = ctk.StringVar(value="")
        self.noteVar     = ctk.StringVar(value="")
        self.messageVar  = ctk.StringVar(value="")

        # Vars de cadastro
        self.si_usernameVar = ctk.StringVar()
        self.si_emailVar = ctk.StringVar()
        self.si_ageVar = ctk.StringVar()
        self.si_passwordVar = ctk.StringVar()

        # Frames
        self.loginFrame = None
        self.signupFrame = None
        self.dashboardFrame = None
        self.transactionFrame = None
        self.extractFrame = None

        # Inicia na tela de login
        self.createLoginFrame()
        self.show_frame(self.loginFrame)

    # -------- Helpers --------
    def show_frame(self, frame_to_show: ctk.CTkFrame):
        for fr in [self.loginFrame, self.signupFrame, self.dashboardFrame, self.transactionFrame, self.extractFrame]:
            if fr is not None:
                fr.pack_forget()
        frame_to_show.pack(pady=20, padx=24, fill="both", expand=True)
        self.messageVar.set("")

    def parse_amount(self) -> Decimal:
        try:
            return parse_amount_str(self.amountVar.get())
        except (InvalidOperation, AttributeError):
            raise ValueError("Informe um valor numérico válido. Ex.: 100.50")

    # -------- Ações --------
    def do_login(self):
        username = self.usernameVar.get().strip()
        pwd = self.passwordVar.get()

        if not username:
            self.messageVar.set("Informe um usuário.")
            return

        row = self.storage.get_user_by_username(username)
        if not row:
            self.messageVar.set("Usuário não encontrado. Cadastre-se.")
            return

        if row.get("password_hash") != hash_password(pwd):
            self.messageVar.set("Senha inválida.")
            return

        # cria cliente e registra login
        self.current_client = Client(row, self.storage)
        self.storage.set_login_time(self.current_client.user_id)

        self.createDashboardFrame()
        self.show_frame(self.dashboardFrame)
        self.refresh_dashboard()

    def do_logout(self):
        if self.current_client:
            self.storage.set_logout_time(self.current_client.user_id)
        self.current_client = None
        self.usernameVar.set("")
        self.passwordVar.set("")
        self.amountVar.set("")
        self.noteVar.set("")
        if self.loginFrame is None:
            self.createLoginFrame()
        self.show_frame(self.loginFrame)

    def do_open_signup(self):
        if self.signupFrame is None:
            self.createSignupFrame()
        self.show_frame(self.signupFrame)

    def do_signup(self):
        try:
            username = self.si_usernameVar.get().strip()
            email = self.si_emailVar.get().strip()
            age_s = self.si_ageVar.get().strip()
            pwd = self.si_passwordVar.get()

            if not username or not email or not age_s or not pwd:
                self.messageVar.set("Preencha todos os campos de cadastro.")
                return
            age = int(age_s)
            if age <= 0:
                self.messageVar.set("Idade inválida.")
                return

            user = self.storage.create_user(
                username=username,
                email=email,
                age=age,
                password_hash=hash_password(pwd),
            )
            self.messageVar.set("Cadastro realizado. Faça login.")
            # limpa campos de cadastro
            self.si_usernameVar.set("")
            self.si_emailVar.set("")
            self.si_ageVar.set("")
            self.si_passwordVar.set("")
            self.show_frame(self.loginFrame)
        except ValueError as e:
            self.messageVar.set(str(e))
        except Exception as e:
            self.messageVar.set(f"Erro no cadastro: {e}")

    def do_open_deposit(self):
        self.createTransactionFrame(mode="DEPOSIT")
        self.show_frame(self.transactionFrame)

    def do_open_withdraw(self):
        self.createTransactionFrame(mode="WITHDRAW")
        self.show_frame(self.transactionFrame)

    def do_confirm_transaction(self, mode: str):
        if self.current_client is None:
            self.messageVar.set("Nenhum cliente logado.")
            return
        try:
            amount = self.parse_amount()
            note = self.noteVar.get().strip()
            if mode == "DEPOSIT":
                self.current_client.deposit(amount, note)
                self.messageVar.set("Depósito realizado.")
            else:
                self.current_client.withdraw(amount, note)
                self.messageVar.set("Saque realizado.")
            self.amountVar.set("")
            self.noteVar.set("")
            self.refresh_dashboard()
            self.show_frame(self.dashboardFrame)
        except ValueError as e:
            self.messageVar.set(str(e))

    def do_open_extract(self):
        self.createExtractFrame()
        self.show_frame(self.extractFrame)

    def refresh_dashboard(self):
        if self.dashboardFrame is not None and self.current_client is not None:
            self.name_lbl.configure(text=f"Conta de {self.current_client.name}")
            self.bal_lbl.configure(text=f"Saldo: {br_money(self.current_client.balance)}")

    # -------- Telas --------
    def createLoginFrame(self):
        self.loginFrame = ctk.CTkFrame(master=self)

        ctk.CTkLabel(self.loginFrame, text="Login", font=("Arial", 20, "bold")).pack(pady=(12, 6))
        ctk.CTkEntry(self.loginFrame, placeholder_text="Usuário", textvariable=self.usernameVar).pack(pady=8, padx=10)
        ctk.CTkEntry(self.loginFrame, placeholder_text="Senha", show="*", textvariable=self.passwordVar).pack(pady=8, padx=10)

        row = ctk.CTkFrame(self.loginFrame)
        row.pack(pady=12)
        ctk.CTkButton(row, text="Entrar", width=140, command=self.do_login).grid(row=0, column=0, padx=8, pady=8)
        ctk.CTkButton(row, text="Cadastrar", width=140, command=self.do_open_signup).grid(row=0, column=1, padx=8, pady=8)

        ctk.CTkLabel(self.loginFrame, textvariable=self.messageVar, text_color="orange").pack(pady=(6, 0))

    def createSignupFrame(self):
        self.signupFrame = ctk.CTkFrame(master=self)

        ctk.CTkLabel(self.signupFrame, text="Cadastro (Sign-in)", font=("Arial", 20, "bold")).pack(pady=(12, 6))
        ctk.CTkEntry(self.signupFrame, placeholder_text="Usuário", textvariable=self.si_usernameVar).pack(pady=6, padx=10)
        ctk.CTkEntry(self.signupFrame, placeholder_text="E-mail", textvariable=self.si_emailVar).pack(pady=6, padx=10)
        ctk.CTkEntry(self.signupFrame, placeholder_text="Idade", textvariable=self.si_ageVar).pack(pady=6, padx=10)
        ctk.CTkEntry(self.signupFrame, placeholder_text="Senha", show="*", textvariable=self.si_passwordVar).pack(pady=6, padx=10)

        row = ctk.CTkFrame(self.signupFrame)
        row.pack(pady=12)
        ctk.CTkButton(row, text="Criar conta", command=self.do_signup).grid(row=0, column=0, padx=8)
        ctk.CTkButton(row, text="Voltar", command=lambda: self.show_frame(self.loginFrame)).grid(row=0, column=1, padx=8)

        ctk.CTkLabel(self.signupFrame, textvariable=self.messageVar, text_color="orange").pack(pady=(6, 0))

    def createDashboardFrame(self):
        self.dashboardFrame = ctk.CTkFrame(master=self)

        self.name_lbl = ctk.CTkLabel(self.dashboardFrame, text="Conta", font=("Arial", 18, "bold"))
        self.name_lbl.pack(pady=(12, 6))
        self.bal_lbl = ctk.CTkLabel(self.dashboardFrame, text="Saldo: R$ 0,00", font=("Arial", 20))
        self.bal_lbl.pack(pady=6)

        btns = ctk.CTkFrame(self.dashboardFrame)
        btns.pack(pady=16)
        ctk.CTkButton(btns, text="Depositar", width=160, command=self.do_open_deposit).grid(row=0, column=0, padx=8, pady=8)
        ctk.CTkButton(btns, text="Sacar", width=160, command=self.do_open_withdraw).grid(row=0, column=1, padx=8, pady=8)
        ctk.CTkButton(btns, text="Extrato", width=160, command=self.do_open_extract).grid(row=1, column=0, padx=8, pady=8)
        ctk.CTkButton(btns, text="Sair", width=160, command=self.do_logout).grid(row=1, column=1, padx=8, pady=8)

        ctk.CTkLabel(self.dashboardFrame, textvariable=self.messageVar, text_color="orange").pack(pady=(6, 0))

    def createTransactionFrame(self, mode: str):
        self.transactionFrame = ctk.CTkFrame(master=self)

        title = "Depósito" if mode == "DEPOSIT" else "Saque"
        ctk.CTkLabel(self.transactionFrame, text=title, font=("Arial", 18, "bold")).pack(pady=(12, 6))

        ctk.CTkEntry(self.transactionFrame, placeholder_text="Valor (ex.: 100,50)", textvariable=self.amountVar).pack(pady=8, padx=10)
        ctk.CTkEntry(self.transactionFrame, placeholder_text="Observação (opcional)", textvariable=self.noteVar).pack(pady=8, padx=10)

        row = ctk.CTkFrame(self.transactionFrame)
        row.pack(pady=12)
        ctk.CTkButton(row, text="Confirmar", command=lambda: self.do_confirm_transaction(mode)).grid(row=0, column=0, padx=8)
        ctk.CTkButton(row, text="Cancelar", command=lambda: self.show_frame(self.dashboardFrame)).grid(row=0, column=1, padx=8)

        ctk.CTkLabel(self.transactionFrame, textvariable=self.messageVar, text_color="orange").pack(pady=(6, 0))

    def createExtractFrame(self):
        self.extractFrame = ctk.CTkFrame(master=self)
        ctk.CTkLabel(self.extractFrame, text="Extrato", font=("Arial", 18, "bold")).pack(pady=(12, 6))

        box = ctk.CTkTextbox(self.extractFrame, height=260)
        box.pack(fill="both", expand=True, padx=10, pady=10)

        if self.current_client:
            df = self.storage.get_transactions(self.current_client.user_id)
            if df.empty:
                box.insert("end", "Sem movimentos até o momento.\n")
            else:
                # mais recente primeiro
                df = df.sort_values("timestamp", ascending=False)
                for _, r in df.iterrows():
                    kind = r["kind"]
                    sign = "+" if kind == "DEPOSIT" else "-"
                    amt = Decimal(r["amount"])
                    ts = r["timestamp"]
                    note = r.get("note") or ""
                    line = f"[{ts}] {kind}: {sign}{br_money(amt)}"
                    if note:
                        line += f" — {note}"
                    line += f" (Saldo após: {br_money(Decimal(r['balance_after']))})\n"
                    box.insert("end", line)
        else:
            box.insert("end", "Sem usuário logado.\n")

        ctk.CTkButton(self.extractFrame, text="Voltar", command=lambda: self.show_frame(self.dashboardFrame)).pack(pady=8)

# -------------------- Main --------------------
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
