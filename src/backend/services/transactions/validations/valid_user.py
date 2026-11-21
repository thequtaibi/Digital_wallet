import sqlite3
from src.backend.services.accounts.users.user import AccountLimits, AccountType


class Validations:
    DATABASE_PATH = "src/backend/database/wallet.db"
    ACCOUNT_LIMITS = AccountLimits.ACCOUNT_LIMITS

    @staticmethod
    def _connect():
        conn = sqlite3.connect(Validations.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def pull_data(user_id):
        """Return the user row as a dict, or None if not found."""
        conn = Validations._connect()
        try:
            row = conn.execute(
                "SELECT * FROM users WHERE user_id = ? LIMIT 1",
                (user_id,),
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def valid_users(user_id):
        return Validations.pull_data(user_id) is not None

    @staticmethod
    def validate_amount(user_id, amount):
        """True if today's total plus the new amount stays within the daily limit."""
        user = Validations.pull_data(user_id)
        if user is None:
            return False

        try:
            account_type = AccountType(user["account_type"])
        except ValueError: 
            return False

        limit = Validations.ACCOUNT_LIMITS.get(account_type)
        if limit is None:
            return False

        conn = Validations._connect()
        try:
            today_total = conn.execute(
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

        return today_total + amount <= limit

    @staticmethod
    def valid_idempotency_key(idempotency_key):
        conn = Validations._connect()
        try:
            row = conn.execute(
                "SELECT 1 FROM transactions WHERE idempotency_key = ? LIMIT 1",
                (idempotency_key,),
            ).fetchone()
            return row is None
        finally:
            conn.close()

    @staticmethod
    def validate_account(user_id, amount):
        user = Validations.pull_data(user_id)
        if user is None:
            return False
        if user["account_status"] == 0:
            return False
        return Validations.validate_amount(user_id, amount)