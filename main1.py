import streamlit as st
import sqlite3
import hashlib
import subprocess
import base64

# ✅ Database Connection (Using my.db)
def get_db_connection():
    conn = sqlite3.connect("D:/project_finalize/database/my.db", check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()  # Ensure table is created before inserting users
    return conn

# ✅ Hashing passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Set background image
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
        .stTextInput label, .stButton > button {{
            font-size: 18px !important;
            font-weight: bold !important;
            width: 200px !important;
            height: 50px !important;
            border-radius: 10px !important;
            color: white !important;
            background-color: #FF5733 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Apply background image
add_bg_from_local(r"D:\project_finalize\assets\images2.jpg")

# ✅ Page Title
st.title("🚗 Car Parking Management")

# ✅ Centered Layout for Login & Signup Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🔐 Login"):
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/user/userin/login.py"])

with col2:
    if st.button("📝 Register"):
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/user/userin/register.py"])
