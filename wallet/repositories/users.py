import sqlite3
from wallet.config import DatabasePath


def insert_user(user):
    """Save a new Account into the users table. (moved from AccountService.save_to_db)"""
    with sqlite3.connect(DatabasePath.PATH) as conn:
            conn.execute(
                """
                INSERT INTO users (
                    user_id,
                    account_number,
                    balance,
                    currency,
                    account_status,
                    gov_identification,
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    username,
                    password,
                    created_at,
                    account_type
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user.user_id,
                    user.account_number,
                    user.balance,
                    user.currency,
                    user.account_status,
                    user.gov_identification,
                    user.first_name,
                    user.last_name,
                    user.email,
                    user.phone_number,
                    user.username,
                    user.password,
                    user.created_at,
                    user.account_type.value
                )
                    )


def gov_id_exists(gov_identification):
    """True if an account with this ID number exists. (moved from AccountService.check_for_existing_account)"""
    with sqlite3.connect(DatabasePath.PATH) as conn:
        result = conn.execute(
            """
            SELECT 1
            FROM users
            WHERE gov_identification = ?
            LIMIT 1
            """,
            (gov_identification,)
        )

        return result.fetchone() is not None


def find_login(username):
    """Return the (username, password) rows for this username. (moved from LoginVerification._search_db)"""
    with sqlite3.connect(DatabasePath.PATH) as conn:
        result = conn.execute("""
                SELECT
                username,
                password
                FROM users
                WHERE username = ?
                """,
                (username,))
        return result.fetchall()


def get_by_id(user_id):
    """Return the user row as a dict, or None if not found. (moved from Validations.pull_data)"""
    conn = sqlite3.connect(DatabasePath.PATH)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE user_id = ? LIMIT 1",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_by_gov_id(gov_identification):
    """Return the user row as a dict, or None if not found. (moved from api/accounts.py account_informations)"""
    with sqlite3.connect(DatabasePath.PATH) as conn:
        conn.row_factory = sqlite3.Row

        result = conn.execute(
            "SELECT * FROM users WHERE gov_identification = ?",
            (gov_identification,)
        )

        user = result.fetchone()
        return dict(user) if user else None


def move_balance(debtor, creditor, amount):
    """Take `amount` from debtor and add it to creditor, in ONE database transaction.
    If any step fails, nothing changes. (moved from TransferService.transfer_process)"""
    with sqlite3.connect(DatabasePath.PATH) as conn:

        conn.execute("BEGIN IMMEDIATE")

        sender = conn.execute(
            """
            UPDATE users
            SET balance = balance - ?
            WHERE user_id = ? AND balance >= ?
            """,
            (
                amount,
                debtor,
                amount
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
                amount,
                creditor
            )
        )

        if receiver.rowcount != 1:
            raise ValueError("Receiver not found")


def add_to_balance(user_id, amount):
    """Add `amount` to this user's balance. True if the user was found. (moved from Deposit._transfer_process)"""
    with sqlite3.connect(DatabasePath.PATH) as conn:
        result = conn.execute(
            """
            UPDATE users
            SET balance = balance + ?
            WHERE user_id = ?
            """,
            (
                amount,
                user_id,)
        )
    return result.rowcount == 1
