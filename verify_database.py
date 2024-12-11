import sqlite3

conn = sqlite3.connect("data/database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM interactions;")
rows = cursor.fetchall()
if rows:
    print("Data in interactions table:", rows)
else:
    print("No data found in interactions table.")

conn.close()
