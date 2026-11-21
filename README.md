# Digital Wallet

A small wallet backend I built to learn how money apps work. Python, Flask, SQLite.
It's a learning project, so don't use it with real money.

## What it does

- Create accounts and log in (passwords hashed with Argon2)
- Deposit and transfer money, with a daily limit per account type
- Show a user's transaction history

Transfers can't double-spend: the balance check and update are one SQL statement
inside a locked transaction. Each payment needs an `idempotency_key`, so the same
request can't go through twice.

## Structure

- `wallet/api/` handles requests
- `wallet/services/` holds the rules
- `wallet/repositories/` is the only code that talks to the database

## Run it

Needs Python 3.14+.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdir -p database
python -c "import sqlite3; sqlite3.connect('database/wallet.db').executescript(open('wallet/schema.sql').read())"
python run.py
```

## Endpoints

| Method | Path | Body |
|---|---|---|
| POST | `/accounts` | `gov_identification, first_name, last_name, email, phone_number, username, password` |
| GET | `/accounts/<gov_identification>` | |
| POST | `/login` | `username, password` |
| POST | `/transactions/transfers` | `transaction_type` (`deposit` or `transfer`), `idempotency_key, debtor, creditor, amount` |
| POST | `/transactions/report` | `user_id` |

## Not done yet

- No login token, so endpoints trust any `user_id` sent to them
- `GET /accounts` returns the password hash
- Some errors return 500 instead of a clear message
- Money is stored as float, not cents
- No tests or withdraw yet
