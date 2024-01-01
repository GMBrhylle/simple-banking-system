class BankAccount:

    def __init__(self, account_id, client_id, account_type, balance=0.0):
        self.account_id = account_id
        self.client_id = client_id
        self.account_type = account_type
        self.balance = balance

    def getBalance(self):
        return self.balance

    def getTypeofAccount(self):
        return self.account_type

    def getIDNumber(self):
        return self.account_id

    def printDetails(self):
        print(f"Account ID # {self.account_id}")
        print(f"Client ID # {self.client_id}")
        print(f"Account Type: {self.account_type}")
        print(f"Balance: {self.balance}")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False
