import uuid
import time
import sqlite3
from src.backend.services.transactions.transactions_operations.recorded_transactions import RecordedTransactions
from src.backend.services.transactions.transactions_operations.transfer_info import TransferInfo
from datetime import datetime


class TransferService:
    def __init__(self, transactionInfo):
        self.transaction_id = str(uuid.uuid4().int)
        self.transaction_type = transactionInfo.transaction_type
        self.debtor = transactionInfo.debtor
        self.creditor = transactionInfo.creditor
        self.amount = transactionInfo.amount
        self.status = None
        self.created_at = time.time()
        self.idempotency_key = transactionInfo.idempotency_key



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

    def validate_transfer(self):
        if self.debtor == self.creditor:
            return "Cannot transfer to the same account."

        if not self.valid_users(self.debtor):
            return "Sender account not found."

        if not self.valid_users(self.creditor):
            return "Recipient account not found."

        if self.amount < 1:
            return "Invalid transfer amount."

        return None

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

        message = self.validate_transfer()

        if message is not None:
            self.status = "failed"
            recorded_transactions.record(status=self.status, note=message)
            return message

        if self.transfer_process():
            self.status = "completed"
            recorded_transactions.record(status=self.status, note="Transfer completed successfully.")
            return f"{"Transfer completed successfully."}"

        self.status = "failed"
        return "Transfer failed"


        
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
        


