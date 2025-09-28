from datetime import datetime

# Need to add the date period organizing by day and the emission by day interval.

DATE_FMT = "%Y-%m-%d %H:%M:%S"

class Extract:

    def __init__(self):
        self.extractText = []
        
    def generate(self, status, now, kind, amount, balance):
        self.extractText.append({"status":status, "date":now, "kind":kind, "value":amount, "balance":balance})

    def show(self):
        for i in self.extractText:
            print(i)