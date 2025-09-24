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


class ClientAccount:
    """Backend da conta do cliente: saldo, transações e extrato"""
    def __init__(self, owner: str):
        self.owner = owner
        self._balance = Decimal("0.00")
        self._extract: list[Transaction] = []

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def extract(self) -> list[Transaction]:
        return self._extract

    def _quantize(self, value: Decimal) -> Decimal:
        """Arredonda valores monetários para 2 casas decimais"""
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def deposit(self, value: float, note: str = "") -> Transaction:
        """Deposita um valor positivo"""
        amount = self._quantize(Decimal(str(value)))
        if amount <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")

        self._balance += amount
        tx = Transaction("DEPÓSITO", amount, self._balance, note)
        self._extract.append(tx)
        return tx

    def withdraw(self, value: float, note: str = "") -> Transaction:
        """Saque: só permitido se houver saldo"""
        amount = self._quantize(Decimal(str(value)))
        if amount <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if amount > self._balance:
            raise ValueError("Saldo insuficiente para saque.")

        self._balance -= amount
        tx = Transaction("SAQUE", amount, self._balance, note)
        self._extract.append(tx)
        return tx

    def get_extract(self) -> list[str]:
        """Retorna extrato formatado como lista de strings"""
        if not self._extract:
            return ["Nenhum movimento."]
        return [str(tx) for tx in self._extract]
