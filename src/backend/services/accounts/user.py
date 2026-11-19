import uuid
import time
from argon2 import PasswordHasher
import sqlite3
from .user_validator import UserValidator

"""TODO
vailed email
vailed phone number + add +966
vailed password
"""


class User:
    def __init__(self, gov_identification, first_name, last_name, email, phone_number, password, balance=0):
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
        self.password = PasswordHasher().hash(password)
        self.created_at = time.time()



class UserService:
    LIMIT = 10000
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
                            password,
                            created_at
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                            self.user.password,
                            self.user.created_at
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
        
        elif not UserValidator().validate_email(self.user.email):
            return "invild email" 

        elif not UserValidator().validate_phone_number(self.user.phone_number):
            return 'invild phone'
        else:
            save_to_db = self.save_to_db()
            return save_to_db


    def delete_account(self):
        pass

    def edit_account(self):
        pass