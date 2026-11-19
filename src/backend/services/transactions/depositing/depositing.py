import uuid
import time
import sqlite3
from src.backend.services.transactions.transactions_operations.recorded_transactions import RecordedTransactions
from src.backend.services.transactions.transactions_operations.transfer_info import TransferInfo
from datetime import datetime
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
            return False
        
        if not Validations.valid_users(self.creditor):
            return False

        if self.amount < 1:
            return False

        return None

    def deposit(self):

        if not Validations.valid_idempotency_key(self.idempotency_key):
            raise ValueError("Erorr")

        
        recorded_transactions = RecordedTransactions(
                    transaction_id=self.transaction_id,
                    transaction_type=self.transaction_type,
                    debtor=self.debtor,
                    creditor=self.creditor,
                    amount=self.amount,
                    created_at=self.created_at,
                    idempotency_key=self.idempotency_key
                )
        
        
        message = self._validate_transfer()

        
        
        if message is not None:
            self.status = "failed"
            recorded_transactions.record(status=self.status, note=message)
            return False

        if self._transfer_process():
            self.status = "completed"
            recorded_transactions.record(status=self.status, note=message)
            return True
        
        self.status = "failed"
        return False

    def report(self, note):
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


