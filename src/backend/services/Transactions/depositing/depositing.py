import uuid
import time
import sqlite3
from src.backend.services.Transactions.recorded_transactions import RecordedTransactions
from src.backend.services.Transactions.transfer_info import TransferInfo


class Deposit:
    DATABASE_PATH = "/home/kind/Desktop/Digital_Wallet/src/backend/database/wallet.db"
    def __init__(self, TransferInfo):
        self.transaction_id = str(uuid.uuid4().int)
        self.atm_id = TransferInfo.debtor
        self.user_id = TransferInfo.creditor
        self.transaction_type = TransferInfo.transaction_type
        self.amount = TransferInfo.amount
        self.status = None
        self.created_at = time.time()
        self.idempotency_key = str(uuid.uuid7())

    def valid_users(self, account_id):
        with sqlite3.connect(self.DATABASE_PATH) as conn:
            result = conn.execute(
                "SELECT 1 FROM users WHERE user_id = ? LIMIT 1",
                (account_id,)
            )

            return result.fetchone() is not None

    def transfer_process(self):
        with sqlite3.connect(self.DATABASE_PATH) as conn:
            result = conn.execute(
                """
                UPDATE users
                SET balance = balance + ?
                WHERE user_id = ?
                """,
                (
                    self.amount,
                    self.user_id,                )
            )
        return result.rowcount == 1


    def deposit(self):
        recorded_transactions = RecordedTransactions(
                    self.transaction_id,
                    self.transaction_type,
                    self.atm_id,
                    self.user_id,
                    self.amount,
                    self.created_at,
                    self.idempotency_key
                )
        
        if self.valid_users(self.user_id):
            if self.amount > 0:
                if self.transfer_process():
                    self.status = "completed"
                    recorded_transactions.recorded(self.status)
                    return {"message":" successfully done"}
                else:
                     self.status = "failed"
                     recorded_transactions.recorded(self.status)
                     return {"message":" Erorr"}
            else:
                self.status = "failed"
                recorded_transactions.recorded(self.status)
                return {"message":" You cant deposit 0"}
        else:
            self.status = "failed"
            recorded_transactions.recorded(self.status)
            return {"message":" You don't have account"}



