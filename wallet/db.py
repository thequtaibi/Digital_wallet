import sqlite3
from wallet.config import DatabasePath

def get_connection():
    conn = sqlite3.connect(DatabasePath.PATH)
    conn.row_factory = sqlite3.Row          # rows act like dicts
    conn.execute("PRAGMA foreign_keys = ON")
    return conn