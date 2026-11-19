import sqlite3

class Validations:
    DATABASE_PATH = "/home/kind/Desktop/Digital_Wallet/src/backend/database/wallet.db"

    @classmethod
    def valid_users(account_id):
        with sqlite3.connect(Validations.DATABASE_PATH) as conn:
            result = conn.execute(
                "SELECT 1 FROM users WHERE user_id = ? LIMIT 1",
                (account_id,)
            )
        return result.fetchone() is not None

    @classmethod
    def valid_idempotency_key(idempotency_key):
        with sqlite3.connect(Validations.DATABASE_PATH) as conn:
            result = conn.execute(
                "SELECT 1 FROM users WHERE idempotency_key = ? LIMIT 1",
                (idempotency_key,)
            )
        return result.fetchone() is not None
    