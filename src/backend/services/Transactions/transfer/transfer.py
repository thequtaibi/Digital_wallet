import uuid
import time
import sqlite3
from services.Transactions.recorded_transactions import RecordedTransactions
from services.Transactions.transfer_info import TransferInfo

class TransferService:
    def __init__(self, transactionInfo):
        self.transaction_id = str(uuid.uuid4().int)
        self.transaction_type = transactionInfo.transaction_type
        self.debtor = transactionInfo.debtor
        self.creditor = transactionInfo.creditor
        self.amount = transactionInfo.amount
        self.status = None
        self.created_at = time.time()
        self.idempotency_key = str(uuid.uuid7())



    def valid_users(self, account_id):
        with sqlite3.connect("/home/kind/Desktop/Digital_Wallet/src/backend/database/wallet.db") as conn:
            result = conn.execute(
                "SELECT 1 FROM users WHERE user_id = ? LIMIT 1",
                (account_id,)
            )

            return result.fetchone() is not None

    def transfer_process(self):

        if self.amount <= 0:
            raise ValueError("Amount must be positive")

        if self.debtor == self.creditor:
            raise ValueError("Cannot transfer to the same account")

        with sqlite3.connect("/home/kind/Desktop/Digital_Wallet/src/backend/database/wallet.db") as conn:

            conn.execute("BEGIN IMMEDIATE")

            sender = conn.execute(
                """
                UPDATE users
                SET balance = balance - ?
                WHERE user_id = ? AND balance >= ?
                """,
                (
                    self.amount,
                    self.debtor,
                    self.amount
                )
            )

            if sender.rowcount != 1:
                raise ValueError(
                    "Insufficient balance or sender not found"
                )

            receiver = conn.execute(
                """
                UPDATE users
                SET balance = balance + ?
                WHERE user_id = ?
                """,
                (
                    self.amount,
                    self.creditor
                )
            )

            if receiver.rowcount != 1:
                raise ValueError("Receiver not found")

        return True

    def transfer(self):
        recorded_transactions = RecordedTransactions(
            self.transaction_id,
            self.transaction_type,
            self.debtor,
            self.creditor,
            self.amount,
            self.created_at,
            self.idempotency_key
        )

        
        if (
            self.valid_users(self.debtor) and self.valid_users(self.creditor)
        ):
            if self.transfer_process():
               self.status = "completed"
               recorded_transactions.recorded(self.status)
               return True
            else:
                self.status = "failed"
                recorded_transactions.recorded(self.status)
                return False
            
        else:
            self.status = "failed"
            recorded_transactions.recorded(self.status)
            return False

    def print_report(self):
        pass


test_user = TransferInfo("01a1cfac-cd84-7381-a899-cffb2cc7be84", "01a1d3b5-7765-7505-a358-b41c045e7d18", 10, "transfer")
answer = TransferService(test_user).transfer()
print(answer)
