import uuid
import time
from argon2 import PasswordHasher
import sqlite3
from src.backend.services.accounts.users.vaildations.user_validator import AccountValidator

from enum import Enum

from enum import Enum

class AccountType(Enum):
    NORMAL = "normal"
    SILVER = "silver"
    GOLD = "gold"

ACCOUNT_LIMITS = {
    AccountType.NORMAL: 10_000,
    AccountType.SILVER: 100_000,
    AccountType.GOLD: 1_000_000,
}

def get_account_type(balance: float) -> AccountType:
    if balance < 0:
        raise ValueError("Balance cannot be negative")
    for account_type, limit in ACCOUNT_LIMITS.items():
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



class AccountService:
    DB_PATH = "src/backend/database/wallet.db"
    def __init__(self, user):
        self.user = user


    def save_to_db(self):
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                    conn.execute(
                        """
                        INSERT INTO users (
                            user_id,
                            account_number,
                            balance,
                            currency,
                            account_status,
                            gov_identification,
                            first_name,
                            last_name,
                            email,
                            phone_number,
                            username,
                            password,
                            created_at,
                            account_type
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            self.user.user_id,
                            self.user.account_number,
                            self.user.balance,
                            self.user.currency,
                            self.user.account_status,
                            self.user.gov_identification,
                            self.user.first_name,
                            self.user.last_name,
                            self.user.email,
                            self.user.phone_number,
                            self.user.username,
                            self.user.password,
                            self.user.created_at,
                            self.user.account_type.value
                        )
                            )
            return f"Done adding {self.user.gov_identification}"
          
        except BufferError:
            return f'error {BufferError}'

    def check_for_existing_account(self):
            with sqlite3.connect(self.DB_PATH) as conn:
                result = conn.execute(
                    """
                    SELECT 1
                    FROM users
                    WHERE gov_identification = ?
                    LIMIT 1
                    """,
                    (self.user.gov_identification,)
                )
        
                return result.fetchone() is not None

    def add_account(self):

        if self.check_for_existing_account():
            return "you have already account"
        
        elif not AccountValidator().validate_email(self.user.email):
            return "invild email" 

        elif not AccountValidator().validate_phone_number(self.user.phone_number):
            return 'invild phone'
        else:
            save_to_db = self.save_to_db()
            return save_to_db


    def delete_account(self):
        pass

    def edit_account(self):
        pass