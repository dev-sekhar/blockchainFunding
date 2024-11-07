# src/core/account.py

class Account:
    def __init__(self, account_id, balance=0):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount):
        """Deposit money into the account."""
        self.balance += amount

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def get_balance(self):
        """Return the current balance."""
        return self.balance
