# clientAccount.py
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

DATE_FMT = "%Y-%m-%d %H:%M:%S"

class Transaction:
    """Representa uma transação na conta"""
    def __init__(self, kind: str, amount: Decimal, balance: Decimal, note: str = ""):
        self.kind = kind  # "DEPÓSITO" | "SAQUE"
        self.amount = amount
        self.balance = balance
        self.note = note
        self.timestamp = datetime.now().strftime(DATE_FMT)

    def __str__(self):
        return f"{self.timestamp} | {self.kind}: R$ {self.amount:,.2f} | Saldo: R$ {self.balance:,.2f}"


