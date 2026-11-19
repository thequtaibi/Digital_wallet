import uuid
import time
import sqlite3
from src.backend.services.transactions.transactions_operations.recorded_transactions import RecordedTransactions
from src.backend.services.transactions.transactions_operations.transfer_info import TransferInfo
import datetime
from src.backend.services.transactions.validations.valid_user import Validations

class Deposit:
    DATABASE_PATH = "/home/kind/Desktop/Digital_Wallet/src/backend/database/wallet.db"
    def __init__(self, TransferInfo):
        self.transaction_id = str(uuid.uuid4().int)
        self.debtor = TransferInfo.debtor
        self.creditor = TransferInfo.creditor
        self.transaction_type = "deposit"
        self.amount = TransferInfo.amount
        self.status = None
        self.created_at = time.time()
        self.idempotency_key = TransferInfo.idempotency_key

    #

    def _transfer_process(self):

        if self.amount <= 0:
                    raise ValueError("Amount must be positive")

        if self.debtor == self.creditor:
                    raise ValueError("Cannot transfer to the same account")

        
        with sqlite3.connect(self.DATABASE_PATH) as conn:
            result = conn.execute(
                """
                UPDATE users
                SET balance = balance + ?
                WHERE user_id = ?
                """,
                (
                    self.amount,
                    self.creditor,                )
            )
        return result.rowcount == 1

    def _validate_transfer(self):
        if self.debtor == self.creditor:
            return "Cannot transfer to the same account."
        
        if not Validations.valid_users(self.creditor):
            return "Recipient account not found."

        if self.amount < 1:
            return "Invalid transfer amount."

        if Validations.valid_idempotency_key(self.idempotency_key):
             return "duoblecated operateions"

        return None

    def deposit(self):
        recorded_transactions = RecordedTransactions(
                    self.transaction_id,
                    self.transaction_type,
                    self.debtor,
                    self.creditor,
                    self.amount,
                    self.created_at,
                    self.idempotency_key
                )
        
        
        message = self._validate_transfer()
        if message is not None:
            self.status = "failed"
            recorded_transactions.recorded(status=self.status, note=message)
            return False

        if self._transfer_process():
            self.status = "completed"
            recorded_transactions.recorded(status=self.status, note="True")
            return True
        
        self.status = "failed"
        return False

    def print_report(self, note):
        report = {
            "report_name" : "Transfer Receipt",
            "date" : datetime.fromtimestamp(self.created_at),
            "transaction_id" : self.transaction_id,
            "amount" : self.amount,
            "from": self.debtor,
            "to": self.creditor,
            "status": self.status,
            "note": note
        }

        return report


user = TransferInfo(
     "t1",
     "atm-1",
     "01a1d3b5-7765-7505-a358-b41c045e7d18",
     1000,
     "21d1b862-6223-7307-b06f-1129b387c339"
)
d = Deposit(user)
d.deposit()
if d.deposit():
     print(d.print_report())