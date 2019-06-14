
import sqlite3
conn = sqlite3.connect("coffee_order.db")
cur = conn.cursor()
print(conn ,cur)
cur.execute("Select * from user_ord")
rows = cur.fetchall()
for row in rows:
	print(row)
