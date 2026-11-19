import sqlite3

class RecordedTransactions:
    def __init__(self, transaction_id, transaction_type, debtor, creditor, amount,created_at, idempotency_key):
         self.transaction_id = transaction_id
         self.transaction_type = transaction_type
         self.creditor = creditor
         self.debtor = debtor
         self.amount = amount
         self.created_at = created_at
         self.idempotency_key = idempotency_key
         self.note = None



    def recorded(self, status, note):
            self.note = note
            with sqlite3.connect("/home/kind/Desktop/Digital_Wallet/src/backend/database/wallet.db") as conn:
                result = conn.execute("""
                        INSERT INTO transactions(
                            transaction_id,
                            transaction_type,
                            from_account_id,
                            to_account_id,
                            amount,
                            status,
                            created_at,
                            idempotency_key,
                            note
                        )
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                        self.transaction_id,
                        self.transaction_type,
                        self.creditor,
                        self.debtor,
                        self.amount,
                        status,
                        self.created_at,
                        self.idempotency_key,
                        self.note
                        )
                        )
            return result.rowcount == 1