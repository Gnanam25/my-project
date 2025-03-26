import streamlit as st
import os
import subprocess
import base64
import sqlite3
import pandas as pd

# ✅ Set Page Configuration
st.set_page_config(page_title="Dashboard", page_icon="📋", layout="wide")

# ✅ Function to set background image
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
        .stButton > button {{
            width: 300px !important;
            height: 50px !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local(r"D:\project_finalize\assets\images.jpeg")

# ✅ Database Connection Functions
def get_db_connection(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)

# ✅ Create Tables (If Not Exists)
def create_tables():
    with get_db_connection("D:/project_finalize/database/my.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                login_time TIMESTAMP
            )
        """)
        conn.commit()

    with get_db_connection("D:/project_finalize/database/admin.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                login_time TIMESTAMP
            )
        """)
        conn.commit()

# ✅ Fetch Data Functions
def get_users():
    with get_db_connection("D:/project_finalize/database/my.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, login_time FROM users ORDER BY login_time DESC")
        return cursor.fetchall()

def get_admins():
    with get_db_connection("D:/project_finalize/database/admin.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, login_time FROM admins ORDER BY login_time DESC")
        return cursor.fetchall()

# ✅ Ensure tables exist before querying
create_tables()

# ✅ Initialize Session State
for key in ["show_users", "show_admins", "show_upload"]:
    if key not in st.session_state:
        st.session_state[key] = False

# ✅ Main Dashboard Title
st.title("📊 Parking Management System Dashboard")

# ✅ Create Buttons for Viewing Users/Admins
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 View User Details"):
        st.session_state["show_users"] = True
        st.session_state["show_admins"] = False

with col2:
    if st.button("🔐 View Admin Details"):
        st.session_state["show_users"] = False
        st.session_state["show_admins"] = True

with col3:
    if st.button("🚪 Logout"):
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/admin/stream_log.py"])
        st.stop()

# ✅ Show User Details
if st.session_state["show_users"]:
    st.subheader("👤 User Details")
    users_data = get_users()
    if users_data:
        df_users = pd.DataFrame(users_data, columns=["ID", "Username", "Last Login Time"])
        st.dataframe(df_users, use_container_width=True)  # ✅ Fixes warning
    else:
        st.info("No users found.")

# ✅ Show Admin Details
if st.session_state["show_admins"]:
    st.subheader("🔐 Admin Details")
    admins_data = get_admins()
    if admins_data:
        df_admins = pd.DataFrame(admins_data, columns=["ID", "Username", "Last Login Time"])
        st.dataframe(df_admins, use_container_width=True)  # ✅ Fixes warning
    else:
        st.info("No admins found.")

# ✅ Upload & Processing Section
st.write("---")
st.subheader("📤 Upload & Process Files")

# Ensure directories exist
os.makedirs("uploads_img", exist_ok=True)
os.makedirs("uploads_video", exist_ok=True)

# ✅ Show Upload Page
if st.button("🚀 Upload & Process Files"):
    st.session_state["show_upload"] = True

if st.session_state["show_upload"]:
    st.subheader("📤 Upload Page")

    # ✅ Image Processing
    if st.button("Process Image 📷"):
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/admin/stream_img.py"])

    # ✅ Video Processing
    if st.button("Process Video 🎥"):
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/admin/stream_video.py"])
