class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
        self.balance = 0

    def deposit(self, value:float):
        self.balance += float(value)

    def withdraw(self, value:float):
        self.balance -= float(value)
    

