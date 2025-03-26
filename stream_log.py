import streamlit as st
import sqlite3
import hashlib
import subprocess
import base64

# ✅ Set Page Configuration FIRST
st.set_page_config(page_title="Admin Login", page_icon="🔑")

# ✅ Database File Path
DB_FILE = "D:/project_finalize/database/admin.db"

# ✅ Function to Hash Passwords
def make_hashes(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Function to Verify Admin Login
def login_admin(username, password):
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", 
                   (username, make_hashes(password)))
    result = cursor.fetchone()
    conn.close()
    return result

# ✅ Function to Set Background Image
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
        .stTextInput label, .stButton button, .stMarkdown, .stTitle, .stSuccess, 
        .stError, .stWarning {{
            color: black !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Set Background Image
add_bg_from_local("D:/project_finalize/assets/images.jpeg")

# ✅ Title
st.title("🚪 Admin Login - Car Parking System")

# ✅ Input Fields
username = st.text_input("👤 Admin Username")
password = st.text_input("🔑 Password", type="password")

# ✅ Login Button
if st.button("Login"):
    if login_admin(username, password):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success(f"✅ Logged in as Admin: {username}")
        st.write("Opening Admin Dashboard...")

        # ✅ Open Admin Dashboard
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/admin/stream_upload.py"])
        st.stop()
    else:
        st.error("❌ Invalid Admin Credentials! Please try again.")

# ✅ Logout Button
if st.button("Logout"):
    st.session_state.clear()
    st.success("✅ Successfully logged out!")
    subprocess.Popen(["streamlit", "run", "D:/project_finalize/user/userin/login.py"])
    st.stop()
