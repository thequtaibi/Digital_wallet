import sqlite3
from wallet.config import DatabasePath


class RecordedTransactions:
    DATAPATH = DatabasePath.PATH
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


class TransationsReport:
    def __init__(self, user_id):
        self.user_id = user_id
        # self.from_date = from_date
        # self.to_date = to_date
        self.query = f"""
            SELECT
            u.account_number,
            CONCAT(first_name, ' ', last_name) AS name,
            (SELECT CONCAT(first_name, ' ', last_name) FROM users WHERE user_id = t.creditor) AS "to_account_name",
            (SELECT account_number FROM users WHERE user_id = t.creditor) AS "to_account_num",
            t.amount,
            t.status,
            t.transaction_type,
            t.created_at,
            t.note
            FROM users AS u
            LEFT JOIN transactions AS t
            ON u.user_id = t.debtor
            WHERE u.user_id = ?
            """

    def report(self):
        with sqlite3.connect(DatabasePath.PATH) as conn:
            conn.row_factory = sqlite3.Row
            result = conn.execute(self.query, (self.user_id,))
            transactions = [dict(row) for row in result.fetchall()]
            return transactions


def total_sent_today(user_id):
    """How much this user sent today. (moved from Validations.validate_amount)"""
    conn = sqlite3.connect(DatabasePath.PATH)
    try:
        return conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE debtor = ?
            AND date(created_at, 'unixepoch', 'localtime') = date('now', 'localtime')
            """,
            (user_id,),
        ).fetchone()[0]
    finally:
        conn.close()


def idempotency_key_exists(idempotency_key):
    """True if a transaction with this key was already saved. (moved from Validations.valid_idempotency_key)"""
    conn = sqlite3.connect(DatabasePath.PATH)
    try:
        row = conn.execute(
            "SELECT 1 FROM transactions WHERE idempotency_key = ? LIMIT 1",
            (idempotency_key,),
        ).fetchone()
        return row is not None
    finally:
        conn.close()
