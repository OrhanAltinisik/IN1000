class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def show_balance(self):
        print(self.owner + " has " + str(self.balance) + " kr")

    def deposit(self, amount):
        self.balance += amount
        print(self.owner + " added " + str(amount) + " kr")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(self.owner + " has withdraw " + str(amount) + " kr")
        else:
            print("Not enough money")



account1 = Account("Ola", 500)
account2 = Account("Kari", 1000)

account1.show_balance()
account2.show_balance()
account1.deposit(200)
account1.show_balance()
account1.withdraw(750)
account1.withdraw(650)
account1.show_balance()