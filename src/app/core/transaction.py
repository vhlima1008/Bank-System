from datetime import datetime
from .user import User # WHEN TESTING HERE USE: user (JUST) | REMEMBER TO PUT .user AFTER END TESTS
from .financing import Financing # WHEN TESTING HERE USE: financing (JUST) | REMEMBER TO PUT .financing AFTER END TESTS
from .extract import Extract# WHEN TESTING HERE USE: extract (JUST) | REMEMBER TO PUT .extract AFTER END TESTS

DATE_FMT = "%Y-%m-%d %H:%M:%S"

class Transaction:
    def __init__(self, client:User):
        self.client = client 
        self.financing = Financing()
        self.extract = Extract()
        self.status = ""

    def _now(self) -> str: 
        return datetime.now().strftime(DATE_FMT)
    
    def execute(self, kind:str, amount:float, nParcel:int=1):
        self.status = "refused"
        if amount > 0:
            if kind == "deposit":
                self.status = "aproved"
                self.client.deposit(amount)
            
            elif kind == "withdraw":
                if self.client.balance >= amount:
                    self.status = "aproved"
                    self.client.withdraw(amount)

            elif kind == "financing":
                if amount > 0 and nParcel > 0:
                    self.status = "aproved"
                    return self.financing.simulation(amount, nParcel)
            
            self.extract.generate(self.status, self._now(), kind, amount, self.client.balance)
        else:
            self.extract.generate(self.status, self._now(), kind, amount, self.client.balance)
