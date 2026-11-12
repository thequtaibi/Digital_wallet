import sqlite3


conn = sqlite3.connect('wallet.db')

cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
                  user_id TEXT PRIMARY KEY NOT NULL,
                  account_number INTEGER NOT NULL UNIQUE,
                  balance DOUBLE NOT NULL DEFAULT 0,
                  currency TEXT NOT NULL,
                  account_status BOOLEAN NOT NULL,
                  first_name TEXT NOT NULL,
                  last_name TEXT NOT NULL,
                  email TEXT,
                  phone_number TEXT NOT NULL,
                  password TEXT NOT NULL,
                  created_at DATE,
               )
""")