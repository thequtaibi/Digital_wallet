import uuid
import time
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from argon2 import PasswordHasher
import sqlite3


class User:
    DB_PATH = "/home/kind/Desktop/Digital_Wallet/src/database/wallet.db"

    def __init__(self, gov_identification, first_name, last_name, email, phone_number, password, balance=0):
        self.user_id = str(uuid.uuid7())
        self.account_number = self._generate_account_number()
        self.balance = balance
        self.currency = "USD"
        self.account_status = True
        self.gov_identification = str(gov_identification)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = str(phone_number)
        self.password = self._hash_password(password)
        self.created_at = time.time()

    def _hash_password(self, password):
        return PasswordHasher().hash(password)
    
    def _generate_account_number(self):
        return str(uuid.uuid4().int % 10**10).zfill(10)

    def _check_for_existing_account(self, conn):
        result = conn.execute(
            """
            SELECT 1
            FROM users
            WHERE gov_identification = ?
            LIMIT 1
            """,
            (self.gov_identification,)
        )

        return result.fetchone() is not None


    def _create_table(self, conn):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY NOT NULL,
                account_number TEXT NOT NULL UNIQUE,
                balance REAL NOT NULL DEFAULT 0,
                currency TEXT NOT NULL,
                account_status INTEGER NOT NULL,
                gov_identification TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                phone_number TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)

    def _add_to_db(self, conn):
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
                self.user_id,
                self.account_number,
                self.balance,
                self.currency,
                self.account_status,
                self.gov_identification,
                self.first_name,
                self.last_name,
                self.email,
                self.phone_number,
                self.password,
                self.created_at
            )
        )


    def add_account(self):
        with sqlite3.connect(self.DB_PATH) as conn:
            self._create_table(conn)

            if self._check_for_existing_account(conn):
                print("The account already exists")
                return False

            try:
                self._add_to_db(conn)
            except sqlite3.IntegrityError as error:
                print(f"Account creation failed: {error}")
                return False

            print("Account created successfully")
            return True


    # def update_information(self, account_number= None, gov_identification=None):
    #     with sqlite3.connect(self.DB_PATH) as conn:
    #         if account_number is not None:
    #             result = self._check_for_existing_account(conn , account_number)
    #         elif gov_identification:
    #             result = self._check_for_existing_account(conn , gov_identification)
    #         else:
    #             return "None"

                 




user = User(
    "3422120968",
    "khaled",
    "alquatibi",
    "test@test.com",
    "03432382878",
    "khlk4004",
    1000
)
user.add_account()