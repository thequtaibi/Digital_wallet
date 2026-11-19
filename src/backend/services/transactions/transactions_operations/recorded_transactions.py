import sqlite3

class RecordedTransactions:
    DATAPATH = "/home/kind/Desktop/Digital_Wallet/src/backend/database/wallet.db"
    def __init__(self, transaction_id, transaction_type, debtor, creditor, amount,created_at, idempotency_key):
         self.transaction_id = transaction_id
         self.transaction_type = transaction_type
         self.creditor = creditor
         self.debtor = debtor
         self.amount = amount
         self.created_at = created_at
         self.idempotency_key = idempotency_key
         self.note = None




    def record(self, status, note):
        self.note = note

        with sqlite3.connect(self.DATAPATH) as conn:
            result = conn.execute("""
                INSERT INTO transactions(
                    transaction_id,
                    transaction_type,
                    debtor,
                    creditor,
                    amount,
                    status,
                    created_at,
                    idempotency_key,
                    note
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.transaction_id,
                self.transaction_type,
                self.debtor,
                self.creditor,
                self.amount,
                status,
                self.created_at,
                self.idempotency_key,
                self.note
            ))

        return result.rowcount == 1
