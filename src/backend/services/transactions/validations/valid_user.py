import sqlite3

class Validations:
    DATABASE_PATH = "src/backend/database/wallet.db"

    @staticmethod
    def pull_data(account_id):
        with sqlite3.connect(Validations.DATABASE_PATH) as conn:
            result = conn.execute(
                "SELECT 1 FROM users WHERE user_id = ? LIMIT 1",
                (account_id,)
            )
        return [dict(row) for row in result.fetchall()] is not None

    @staticmethod
    def validate_amount(user_id, acciount_type):
        with sqlite3.connect(Validations.DATABASE_PATH) as conn:
            result = conn.execute(
                """
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE user_id = ? 
                AND date(created_at) = date('now', 'localtime')
                """
                (user_id,)
            )

        
            return result.fetchone()[0] is not None

    @staticmethod
    def valid_idempotency_key(idempotency_key):
        with sqlite3.connect(Validations.DATABASE_PATH) as conn:
            result = conn.execute(
                "SELECT 1 FROM transactions WHERE idempotency_key = ? LIMIT 1",
                (idempotency_key,)
            )

        return result.fetchone() is None


    @staticmethod
    def validate_account(sender_account,amount):
        user_info = Validations.pull_data(sender_account)
        
        if not user_info:
            return "Sender account not found."

        if user_info['account_status'] == 0:
            return "Sender account is inactive."

