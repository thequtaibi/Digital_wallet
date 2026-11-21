import uuid
import time
from enum import Enum
from argon2 import PasswordHasher


class AccountType(Enum):
    NORMAL = "normal"
    SILVER = "silver"
    GOLD = "gold"

class AccountLimits:
    ACCOUNT_LIMITS = {
    AccountType.NORMAL: 10_000,
    AccountType.SILVER: 100_000,
    AccountType.GOLD: 1_000_000,
   }



def get_account_type(balance: float) -> AccountType:
    if balance < 0:
        raise ValueError("Balance cannot be negative")
    for account_type, limit in AccountLimits.ACCOUNT_LIMITS.items():
        if balance <= limit:
            return account_type
    raise ValueError("Balance exceeds the maximum allowed (1,000,000)")

class Account:
    def __init__(self, gov_identification, first_name, last_name, email, phone_number, password, username,balance=0):
        self.user_id = str(uuid.uuid7())
        self.account_number = str(uuid.uuid4().int % 10**10).zfill(10)
        self.balance = balance
        self.currency = "USD"
        self.account_status = True
        self.gov_identification = str(gov_identification)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = str(phone_number)
        self.username = username
        self.password = PasswordHasher().hash(password)
        self.created_at = time.time()
        self.account_type = get_account_type(self.balance)


class TransferInfo:
    def __init__(self, idempotency_key, debtor, creditor, amount, transaction_type):
        self.idempotency_key = idempotency_key
        self.debtor = debtor
        self.creditor = creditor
        if transaction_type in ['deposit', "transfer"]:
            self.transaction_type = transaction_type
        self.amount = amount
