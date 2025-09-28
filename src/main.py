# Need to add login interface
from app.core.transaction import Transaction
from app.core.user import User

client = User("Victor", "victor@email.com", 21)
userTest = Transaction(client)

userTest.execute("deposit", 20)
userTest.execute("withdraw", 30)
userTest.execute("financing", 5000, 3)
userTest.extract.show()