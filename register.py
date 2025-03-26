import streamlit as st
import sqlite3
import hashlib
import subprocess
import base64

# ✅ Database Connection
def get_db_connection():
    conn = sqlite3.connect("D:/project_finalize/database/my.db", check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'  -- ✅ Ensures role is always set
        )
    """)
    conn.commit()
    return conn

# ✅ Hashing Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Background Image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local(r"D:\project_finalize\assets\images2.jpg")

# ✅ Signup Form
st.title("📝 Register - Car Parking Management")
username = st.text_input("👤 Username", placeholder="Enter a unique username").strip().lower()
password = st.text_input("🔑 Password", type="password", placeholder="Enter a strong password")

if st.button("Sign Up"):
    if username and password:
        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Check if username exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.error("❌ Username already exists. Try another one.")
        else:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (username, hash_password(password), "user"))  # ✅ Includes role
            conn.commit()
            st.success("✅ Signup Successful! Proceed to Login.")
            subprocess.Popen(["streamlit", "run", "D:/project_finalize/user/userin/login.py"])

        conn.close()
    else:
        st.warning("⚠️ Please enter both username and password.")

# ✅ Login Redirect Button
if st.button("🔐 Go to Login"):
    subprocess.Popen(["streamlit", "run", "D:/project_finalize/user/userin/login.py"])
