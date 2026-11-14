
import uuid
import time
from argon2 import PasswordHasher
import sqlite3


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

