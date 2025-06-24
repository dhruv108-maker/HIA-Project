# create_users_db.py
import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute('''

''')

conn.commit()
conn.close()
print("✅ users.db created.")
