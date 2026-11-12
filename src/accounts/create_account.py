import uuid
import time
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from argon2 import PasswordHasher
import sqlite3


class CreateAccount:
    def __init__(self, gov_identification, first_name, last_name, email, phone_number, password):
        self.user_id = uuid.uuid7()
        self.account_number = self.__genrated_account_number()
        self.balance = 0
        self.currency = "USD"
        self.account_status = True
        self.gov_identification = gov_identification
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.password = self.__hash_password(password)
        self.created_at = time.time()

    def _hash_password(self, password):
        ph = PasswordHasher()
        return ph.hash(password)

    def _genrated_account_number(self):
        return str(uuid.uuid4().int % 10**10).zfill(10)

    def _check_for_exitst_account(self):
        with sqlite3.connect('database/wallet.db') as conn:
            restlt = conn.execute(
                """
                SELECT 1 
                FROM users 
                WHERE gov_identification = ? 
                LIMIT 1
                """, 
                (self.gov_identification)
                )

        return restlt.fetchone() is not None

    def _add_to_db(self):
        create_table = """"
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY NOT NULL,
                    account_number INTEGER NOT NULL UNIQUE,
                    balance DOUBLE NOT NULL DEFAULT 0,
                    currency TEXT NOT NULL,
                    account_status BOOLEAN NOT NULL,
                    gov_identification INTEGER NOT NULL UNIQUE,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT,
                    phone_number TEXT NOT NULL,
                    password TEXT NOT NULL,
                    created_at DATE,
                )
                    """
        insert_user = """
                    INSERT INTO user (
                        user_id, 
                        account_number, 
                        balance, currency, 
                        account_status,
                        gov_identification,
                        first_name, 
                        last_name, 
                        email , 
                        phone_number ,
                        phone_number ,
                        password ,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

                    """
        with sqlite3.connect('database/wallet.db') as conn:
            conn.execute(create_table)
            conn.execute(
                insert_user, 
                    (
                        self.user_id, 
                        self.account_number, 
                        self.balance, 
                        self.account_status, 
                        self.first_name, 
                        self.last_name, 
                        self.email, 
                        self.phone_number, 
                        self.password, 
                        self.created_at
                    )
                 )

    def process(self):
        pass