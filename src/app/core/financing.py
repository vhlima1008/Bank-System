from typing import List

class Financing:
    def __init__(self, monthlyInterest:float=0.02, contractFee:float=350, monthlyInsurance:float=0.003, FT=True, BST=True):
        self.monthlyInterest = monthlyInterest # 2% a.m.
        self.contractFee = contractFee # 350 BRL
        self.monthlyInsurance = monthlyInsurance # 0,3% a.m.

    def simulation(self, value:float, nParcel:int):
        cF = self.contractFee
        i = self.monthlyInterest
        n = nParcel
        P = value * (i / (1 - (1 + i) ** (-n))) # PRICE Table (without secure)

        balance = value
        tPRICE = []
        for k in range(1, n + 1):
            secure = balance * self.monthlyInsurance
            installments = balance * i
            amort = P - installments
            balance = max(0, balance - amort)
            tPRICE.append({
                "parcel": k,
                "baseValue": round(P, 2),
                "installment": round(installments, 2),
                "amort": round(amort, 2),
                "secure": round(secure, 2),
                "totalParcelValue": round(P + secure, 2),
                "oustandingBalance": round(balance, 2)
            })

        totalPayed = n * (P + secure)
        totalCost = totalPayed + cF

        cashFlows = [value - cF] + [-(P + secure)] * n
        mCET = self._irr(cashFlows)
        aCET = (1 + mCET) ** 12 - 1 if mCET is not None else None

        return {
            "ok": True,
            "params": {
                "value": value,
                "nParcel": nParcel,
                "monthlyInterest": i,
                "contractFee": cF,
                "monthlySecure": secure
            },
            "baseParcel": round(P, 2),
            "withSecureParcel": round(P + secure, 2),
            "totalPayed": round(totalPayed, 2),
            "withContractTotalCost": round(totalCost, 2),
            "monthlyCET": mCET,
            "annualCET": aCET,
            "tablePRICE": tPRICE
        }
            
    def _irr(self, cashFlows:List[float], tol:float=1e-7, maxIter:int=100):
        low, high = -0.99, 2.0

        def npv(rate:float):
            acc = 0.0
            for t, cf in enumerate(cashFlows):
                acc += cf / ((1 + rate) ** t)
            return acc
        
        fLow = npv(low)
        fHigh = npv(high)
        if fLow * fHigh > 0:
            return None
        
        for _ in range(maxIter): # Binary Search for IRR
            mid = (low + high) / 2
            fMid = npv(mid)
            if abs(fMid) < tol:
                return mid
            if fLow * fMid < 0:
                high = mid
                fHigh = fMid
            else:
                low = mid
                fLow = fMid
        return mid
    