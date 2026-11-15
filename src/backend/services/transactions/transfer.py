import uuid
import time
import sqlite3

class transferInfo:
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


    def vaild_users(self, account_id):
        # check if the account exist return Ture
        with sqlite3.connect("src/backend/database/wallet.db") as conn:
            result = conn.execute("SELECT user_id FROM users WHERE user_id = ?" , (account_id,))
        return result.fetchone() is not None


    def transfer_process(self):
        # return True if the sender have enough monany
        if self.amount <= 0:
            raise ValueError("Amount must be positive")

        with sqlite3.connect("src/backend/database/wallet.db") as conn:
            result = conn.execute(
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

            return result.rowcount == 1

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



    def vaildations(self):
        self.status = "pending"
        if self.vaild_users(self.from_account_id) and self.vaild_users(self.to_account_id):
            if self.transfer_process():
               self.status = "completed"
               self.recorded_transactions()
               return "working"
            else:
                self.status = "failed"
                self.recorded_transactions()
                return "not working from transfer_process"
            
        else:
            self.status = "failed"
            self.recorded_transactions()
            return "not working from vaild_users"


tranfor = transferInfo("01a1cfac-cd84-7381-a899-cffb2cc7be84", "01a1d3f3-249d-7033-bd9a-e79b2d738a5d", 500000)
process = TransferService(tranfor).vaildations()
print(process)

class TransactionRepository:
    # create reocted for the Transaction
    pass
