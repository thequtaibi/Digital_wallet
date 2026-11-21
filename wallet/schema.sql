CREATE TABLE IF NOT EXISTS users (
    user_id            TEXT PRIMARY KEY NOT NULL,
    account_number     TEXT NOT NULL UNIQUE,
    balance            REAL NOT NULL DEFAULT 0,
    currency           TEXT NOT NULL,
    account_status     INTEGER NOT NULL,
    gov_identification TEXT NOT NULL UNIQUE,
    first_name         TEXT NOT NULL,
    last_name          TEXT NOT NULL,
    email              TEXT,
    phone_number       TEXT NOT NULL,
    username           VARCHAR(10),
    password           TEXT NOT NULL,
    created_at         REAL NOT NULL,
    account_type       TEXT
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id   TEXT PRIMARY KEY,
    transaction_type TEXT NOT NULL
        CHECK (transaction_type IN ('deposit', 'withdrawal', 'transfer')),
    debtor           INTEGER,
    creditor         INTEGER,
    amount           INTEGER NOT NULL CHECK (amount > 0),
    status           TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'completed', 'failed')),
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    idempotency_key  TEXT NOT NULL UNIQUE,
    note             TEXT,
    FOREIGN KEY (debtor) REFERENCES accounts(id),
    FOREIGN KEY (creditor) REFERENCES accounts(id)
);
