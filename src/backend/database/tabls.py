import sqlite3

with sqlite3.connect("/home/kind/Desktop/Digital_Wallet/src/backend/database/wallet.db") as conn:
    conn.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    transaction_type TEXT NOT NULL
        CHECK (transaction_type IN ('deposit', 'withdrawal', 'transfer')),
    from_account_id INTEGER,
    to_account_id INTEGER,
    amount INTEGER NOT NULL CHECK (amount > 0),
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'completed', 'failed')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    idempotency_key TEXT NOT NULL UNIQUE,
    FOREIGN KEY (from_account_id) REFERENCES accounts(id),
    FOREIGN KEY (to_account_id) REFERENCES accounts(id)
);
""")