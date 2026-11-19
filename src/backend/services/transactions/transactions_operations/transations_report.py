
import sqlite3

class TransationsReport:
    def __init__(self, user_id):
        self.user_id = user_id
        # self.from_date = from_date
        # self.to_date = to_date
        self.query = f"""
            SELECT 
            u.account_number,
            CONCAT(first_name, ' ', last_name) AS name,
            (SELECT CONCAT(first_name, ' ', last_name) FROM users WHERE user_id = t.to_account_id) AS "to_account_name",
            (SELECT account_number FROM users WHERE user_id = t.to_account_id) AS "to_account_num",
            t.amount,
            t.status,
            t.transaction_type,
            t.created_at,
            t.note
            FROM users AS u
            LEFT JOIN transactions AS t
            ON u.user_id = t.from_account_id
            WHERE u.user_id = ? 
            """

    def report(self):
        with sqlite3.connect('/home/kind/Desktop/Digital_Wallet/src/backend/database/wallet.db') as conn:
            conn.row_factory = sqlite3.Row
            result = conn.execute(self.query, (self.user_id,))
            transactions = [dict(row) for row in result.fetchall()]
            return transactions


