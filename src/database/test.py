import sqlite3

conn = sqlite3.connect('/home/kind/Desktop/Digital_Wallet/src/database/wallet.db')

c = conn.execute('SELECT * FROM users').fetchall()
print(c)
conn.close()
