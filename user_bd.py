import sqlite3
import hashlib

# ✅ Define Database File
DB_FILE = "D:/project_finalize/database/my.db"

# ✅ Connect to the Database (Creates it if it doesn’t exist)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# ✅ Create `users` Table (Stores User Logins)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
""")

conn.commit()
conn.close()
print("✅ User Database (`my.db`) Setup Completed!")
