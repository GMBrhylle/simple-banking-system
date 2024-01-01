dela_cruz_finals_case_study/   # Package directory
│
├── __init__.py    # Initializes the package, can be empty or contain package-level documentation or initialization code.
│
├── bank_account.py  # Module for bank account-related classes and functions.
│   ├── class BankAccount:
│   │     def __init__(self, account_number, balance):
│   │         self.account_number = account_number
│   │         self.balance = balance
│   │     def deposit(self, amount):
│   │         # Method to deposit amount to the account
│   │     def withdraw(self, amount):
│   │         # Method to withdraw amount from the account
│
├── bank_client.py   # Module for bank client-related classes and functions.
│   ├── class BankClient:
│   │     def __init__(self, name, accounts):
│   │         self.name = name
│   │         self.accounts = accounts
│   │     def add_account(self, account):
│   │         # Method to add a new account for the client
│
└── bank_system.py   # Module for the overall bank system-related classes and functions.
    ├── class BankSystem:
    │     def __init__(self):
    │         self.clients = []
    │     def add_client(self, client):
    │         # Method to add a new client to the bank system
    │     def remove_client(self, client_id):
    │         # Method to remove a client from the bank system
    │
└── SPECIFICATIONS.pdf  # The specifications document for the project (non-Python file).
