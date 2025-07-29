import sqlite3
conn = sqlite3.connect("db/animaux.db")
cursor = conn.cursor()
cursor.execute("ALTER TABLE animaux ADD COLUMN picture TEXT")
conn.commit()
conn.close()
