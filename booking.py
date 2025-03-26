import streamlit as st
import sqlite3
import cv2
import numpy as np
import easyocr
import os
import base64
import subprocess
import datetime  # ✅ Import datetime for date handling

# ✅ Predefined GPS coordinates & images for each parking slot
PARKING_SLOTS = {
    "Meenakshi Amman Temple - Multi-level Car and Bike Parking": {
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3945.3745!2d78.119776!3d9.919592",
        "image": "D:/project_finalize/assets/meenakshi_parking.jpg",
        "fee": "₹30/hour"
    },
    "ELCOT IT Park, Madurai": {
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3945.64523!2d78.119876!3d9.920987",
        "image": "D:/project_finalize/assets/elcot_parking.jpg",
        "fee": "₹40/hour"
    },
    "AK AHAMED CAR PARKING": {
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3945.6745!2d78.120876!3d9.922345",
        "image": "D:/project_finalize/assets/ahamed_parking.jpg",
        "fee": "₹50/hour"
    }
}

# ✅ Database setup (Using my.db)
def get_db_connection():
    conn = sqlite3.connect("D:/project_finalize/database/my.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # ✅ Ensure the bookings table has booking_date column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT UNIQUE NOT NULL,
            slot_number TEXT NOT NULL,
            fee TEXT NOT NULL DEFAULT '₹0',
            booking_date TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    # ✅ Ensure the admin_notifications table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT NOT NULL,
            slot_number TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    conn.commit()
    return conn


st.title("🚗 Book Parking Slot")

# ✅ Function to set background image
def add_bg_image(main_bg):
    with open(main_bg, "rb") as img_file:
        main_bg_encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{main_bg_encoded});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Set main background only
add_bg_image("D:/project_finalize/assets/images2.jpg")

# ✅ Initialize detected_plate to prevent errors
detected_plate = None

uploaded_file = st.file_uploader("📂 Upload Car Image for OCR", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # ✅ Save uploaded image
    img_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ✅ Read Image and Perform OCR
    image = cv2.imread(img_path)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)

    # ✅ Extract plate number (if detected)
    if result:
        detected_plate = result[0][-2]  # Ensures a valid plate is detected
    else:
        detected_plate = "UNKNOWN"

    st.image(image, caption=f"🔍 Detected Plate: {detected_plate}")

    # ✅ User must enter the plate number manually for validation
    user_plate = st.text_input("📝 Enter Your Vehicle Plate Number (For Confirmation)")

    # ✅ Compare entered plate with detected plate
    if st.button("✅ Confirm Plate Number"):
        if user_plate.strip().upper() == detected_plate.upper():
            st.success("✅ Plate Number Verified! You may proceed with booking.")
        else:
            st.error("❌ Plate Number Mismatch! Please check and try again.")

    # ✅ Show available slots if plate is verified
    if user_plate.strip().upper() == detected_plate.upper():
        st.write("### 🅿️ Available Parking Slots")
        
        # ✅ Display slot images as clickable buttons
        selected_slot = None
        for slot_name, slot_data in PARKING_SLOTS.items():
            st.image(slot_data["image"], caption=f"📍 {slot_name}", use_column_width=True)
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"📍 View Map: {slot_name}"):
                    st.markdown(
                        f'<iframe width="700" height="500" src="{slot_data["map"]}" frameborder="0" allowfullscreen></iframe>',
                        unsafe_allow_html=True
                    )

            with col2:
                if st.button(f"🚗 Book {slot_name}"):
                    selected_slot = slot_name

        # ✅ If a slot is selected, show details
        if selected_slot:
            slot_data = PARKING_SLOTS[selected_slot]
            st.image(slot_data["image"], caption=f"📍 {selected_slot}", use_column_width=True)
            st.write(f"💰 **Fee Structure:** {slot_data['fee']}")

            # ✅ Date selection for booking
            selected_date = st.date_input("📅 Select Parking Date", datetime.date.today())

            if st.button("✅ Confirm Booking"):
                conn = get_db_connection()
                cursor = conn.cursor()

                # ✅ Check if plate is already booked for the same date
                cursor.execute(
                    "SELECT * FROM bookings WHERE plate_number = ? AND booking_date = ?",
                    (detected_plate, str(selected_date))
                )
                existing_booking = cursor.fetchone()

                if existing_booking:
                    st.error(f"❌ This car is already booked on {selected_date}.")
                else:
                    # ✅ Insert booking with selected date
                    cursor.execute(
                        "INSERT INTO bookings (plate_number, slot_number, fee, booking_date, status) VALUES (?, ?, ?, ?, 'Pending')",
                        (detected_plate, selected_slot, slot_data["fee"], str(selected_date))
                    )
                    cursor.execute(
                        "INSERT INTO admin_notifications (plate_number, slot_number, status) VALUES (?, ?, 'Pending')",
                        (detected_plate, selected_slot)
                    )
                    conn.commit()
                    st.success(f"✅ Booking Request Sent for {detected_plate} on {selected_date}!")

                    # ✅ Show clickable Google Maps link
                    st.markdown(f"📍 **[View Directions on Google Maps](https://www.google.com/maps?q={selected_slot})**", unsafe_allow_html=True)

                    # ✅ Embed Google Map in Streamlit
                    st.markdown(
                        f'<iframe width="700" height="500" src="{slot_data["map"]}" frameborder="0" allowfullscreen></iframe>',
                        unsafe_allow_html=True
                    )

                conn.close()

# ✅ Logout Button
st.write("---")
if st.button("🚪 Logout"):
    st.session_state.clear()  # Clear session state
    st.success("✅ Logged out successfully! Redirecting to login page...")
    subprocess.Popen(["streamlit", "run", "D:/project_finalize/main2.py"])
    st.stop()
