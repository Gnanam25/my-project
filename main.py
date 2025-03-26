import streamlit as st
import subprocess
import base64
# Set Streamlit page configuration
st.set_page_config(page_title="Home", page_icon="🏠")

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

add_bg_from_local(r"D:\project_finalize\assets\images.jpeg")
# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Home Page Title
st.title("🏠 Welcome to the Parking Management System 🚗")

st.write("Please log in as a User or Admin to continue.")

# User/Admin Selection
user_type = st.radio("Select Role:", ["User", "Admin"])

# Navigation Buttons
if st.button("Proceed"):
    if user_type == "User":
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/user/main1.py"])  # Redirect User to main1.py
    elif user_type == "Admin":
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/admin/stream_log.py"])  # Redirect Admin to stream_signup.py

# Redirect if authenticated
if st.session_state.authenticated:
    st.success("✅ Authentication successful! Redirecting to upload page...")
    subprocess.Popen(["streamlit", "run", "D:/project_finalize/adminadmin/stream_upload.py"])

