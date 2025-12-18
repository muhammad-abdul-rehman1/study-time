import sqlite3
import os

db_path = 'db.sqlite3'
if not os.path.exists(db_path):
    print("Database not found.")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables starting with socialaccount_
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'socialaccount_%';")
tables = cursor.fetchall()

if not tables:
    print("No socialaccount tables found.")
else:
    for table_name in tables:
        t = table_name[0]
        print(f"Dropping table {t}...")
        cursor.execute(f"DROP TABLE {t}")

conn.commit()
conn.close()
print("Cleaned up socialaccount tables.")
