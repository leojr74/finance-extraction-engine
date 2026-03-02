import sqlite3

conn = sqlite3.connect("finance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
data TEXT,
descricao TEXT,
categoria TEXT,
valor REAL)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS regras(
id INTEGER PRIMARY KEY AUTOINCREMENT,
palavra TEXT,
categoria TEXT)
""")

conn.commit()