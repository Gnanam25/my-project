import sqlite3
import hashlib

# ✅ Define Database File
DB_FILE = "D:/project_finalize/database/admin.db"

# ✅ Connect to the Database (Creates it if it doesn’t exist)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# ✅ Create `admins` Table (Stores Admin Logins)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

# ✅ Predefined Admin Users (Modify if Needed)
admin_users = [
    ("admin1", "adminpass1"),
    ("superadmin", "securepass"),
    ("manager", "manager123"),
]

# ✅ Hash Passwords Before Storing in Database
hashed_admins = [(u, hashlib.sha256(p.encode()).hexdigest()) for u, p in admin_users]

# ✅ Insert Admin Users Only If Table is Empty
cursor.execute("SELECT COUNT(*) FROM admins")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO admins (username, password) VALUES (?, ?)", hashed_admins)
    conn.commit()
    print("✅ Admin users added successfully!")
else:
    print("⚠️ Admin users already exist.")

# ✅ Close Database Connection
conn.close()
print("✅ Admin Database (`admin.db`) Setup Completed!")
