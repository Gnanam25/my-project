import streamlit as st
import sqlite3
import hashlib
import subprocess
import base64
# ✅ Database Connection (Using my.db)
def get_db_connection():
    conn = sqlite3.connect("D:/project_finalize/database/my.db", check_same_thread=False)
    return conn

# ✅ Hashing passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

st.title("🚗 Login - Car Parking Management")
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
         .stTextInput label, .stSelectbox label, .stButton button, .stMarkdown, .stTitle, .stSuccess, .stError, .stWarning {{
             color: black !important;
         }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local(r"D:\project_finalize\assets\images2.jpg")
username = st.text_input("👤 Username", placeholder="Enter your username")
password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

# ✅ Login Button
if st.button("Login"):
    if username and password:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                       (username, hash_password(password)))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.success("✅ Login Successful! Redirecting to Booking Page...")
            subprocess.Popen(["streamlit", "run", "D:/project_finalize/user/userin/booking.py"])  # Redirect to Booking Page
        else:
            st.error("❌ Invalid Username or Password!")
    else:
        st.warning("⚠️ Please enter both username and password.")

# ✅ Signup Redirect Button
if st.button("Go to Signup"):
    subprocess.Popen(["streamlit", "run", "D:/project_finalize/user/userin/register.py"])  # Redirect to Signup Page
