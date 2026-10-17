class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def show_balance(self):
        print(self.owner + " has " + str(self.balance) + " kr")


account1 = Account("Ola", 500)
account2 = Account("Kari", 1000)

account1.show_balance()
account2.show_balance()