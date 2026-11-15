import uuid
import time
import sqlite3

class TransferInfo:
    def __init__(self, from_account_id, to_account_id, amount):
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.transaction_type = "transfer"
        self.amount = amount


class TransferService:
    def __init__(self, transactionInfo):
        self.transaction_id = str(uuid.uuid4().int)
        self.transaction_type = transactionInfo.transaction_type
        self.from_account_id = transactionInfo.from_account_id
        self.to_account_id = transactionInfo.to_account_id
        self.amount = transactionInfo.amount
        self.status = None
        self.created_at = time.time()
        self.idempotency_key = str(uuid.uuid7())






    def valid_users(self, account_id):
        with sqlite3.connect("src/backend/database/wallet.db") as conn:
            result = conn.execute(
                "SELECT 1 FROM users WHERE user_id = ? LIMIT 1",
                (account_id,)
            )

            return result.fetchone() is not None

    def transfer_process(self):

        if self.amount <= 0:
            raise ValueError("Amount must be positive")

        if self.from_account_id == self.to_account_id:
            raise ValueError("Cannot transfer to the same account")

        with sqlite3.connect("src/backend/database/wallet.db") as conn:

            conn.execute("BEGIN IMMEDIATE")

            sender = conn.execute(
                """
                UPDATE users
                SET balance = balance - ?
                WHERE user_id = ? AND balance >= ?
                """,
                (
                    self.amount,
                    self.from_account_id,
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
                    self.to_account_id
                )
            )

            if receiver.rowcount != 1:
                raise ValueError("Receiver not found")

        return True

    def recorded_transactions(self):
        # after process done creater record on the database
        with sqlite3.connect("src/backend/database/wallet.db") as conn:
            result = conn.execute("""
                    INSERT INTO transactions(
                        transaction_id,
                        transaction_type,
                        from_account_id,
                        to_account_id,
                        amount,
                        status,
                        created_at,
                        idempotency_key
                    )
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                    self.transaction_id,
                    self.transaction_type,
                    self.from_account_id,
                    self.to_account_id,
                    self.amount,
                    self.status,
                    self.created_at,
                    self.idempotency_key
                    )
                    )
            return result.rowcount == 1



    def transfer(self):
        self.status = "pending"
        if (
            self.valid_users(self.from_account_id) and self.valid_users(self.to_account_id)
        ):
            if self.transfer_process():
               self.status = "completed"
               self.recorded_transactions()
               return True
            else:
                self.status = "failed"
                self.recorded_transactions()
                return False
            
        else:
            self.status = "failed"
            self.recorded_transactions()
            return False

    def print_report(self):
        pass


test_user = TransferInfo("01a1cfac-cd84-7381-a899-cffb2cc7be84", "01a1d3b5-7765-7505-a358-b41c045e7d18", 500)
answer = TransferService(test_user).transfer()
print(answer)

class TransactionRepository:
    # create reocted for the Transaction
    pass
