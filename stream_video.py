import streamlit as st
import os
import cv2
import numpy as np
import sqlite3
import pickle
from ultralytics import YOLO
import subprocess 
import base64

# Set Page Configurations
st.set_page_config(page_title="Video", page_icon="📤 ")

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

# ========== DATABASE CONNECTION ==========
def get_db_connection():
    return sqlite3.connect("D:/project_finalize/database/admin.db", check_same_thread=False)

# Create Table to Store Parking Slots in admin.db
def create_parking_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x1 INTEGER NOT NULL,
            y1 INTEGER NOT NULL,
            x2 INTEGER NOT NULL,
            y2 INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_parking_table()

# Function to fetch stored parking slots
def get_parking_slots():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT x1, y1, x2, y2 FROM parking_slots")
    slots = cursor.fetchall()
    conn.close()
    return slots

# Load YOLO model
model = YOLO("yolov8n.pt")

# Function to process video and detect occupied/empty slots
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    stframe = st.empty()  # Streamlit placeholder for displaying frames

    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Get frame rate
    frame_interval = int(frame_rate * 10)  # Frames per 10 seconds

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / frame_rate

    st.sidebar.write(f"📌 **Video Duration: {video_duration:.2f} seconds**")

    final_occupied = 0
    final_empty = 0

    parking_slots = get_parking_slots()  # Fetch slots from admin.db

    for frame_num in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break  # Stop if video ends

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run YOLO detection
        results = model(frame)
        detections = results[0].boxes.xyxy.cpu().numpy()

        occupied_boxes = []
        for box in detections:
            if len(box) >= 4:
                x1, y1, x2, y2 = map(int, box[:4])
                occupied_boxes.append((x1, y1, x2, y2))
                cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img_rgb, "Occupied", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        occupied_slots = len(occupied_boxes)

        # Identify empty slots
        empty_slots = []
        if parking_slots:
            for slot in parking_slots:
                if len(slot) == 4:
                    x1, y1, x2, y2 = slot
                    is_occupied = any(
                        ox1 < x2 and ox2 > x1 and oy1 < y2 and oy2 > y1
                        for ox1, oy1, ox2, oy2 in occupied_boxes
                    )
                    if not is_occupied:
                        empty_slots.append(slot)
                        cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img_rgb, "Empty", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        total_slots = len(parking_slots)
        empty_count = len(empty_slots)

        # Show parking stats every 10 seconds
        if frame_num % frame_interval == 0:
            timestamp = frame_num / frame_rate
            st.write(f"📌 **Parking Status at {timestamp:.0f} Seconds**")
            st.write(f"🔹 **Total Slots:** {total_slots}")
            st.write(f"🔴 **Occupied Slots:** {occupied_slots}")
            st.write(f"🟢 **Empty Slots:** {empty_count}")
            st.image(img_rgb, caption=f"Status at {timestamp:.0f} Seconds", channels="RGB", use_container_width=True)

        # Update final counts
        final_occupied = occupied_slots
        final_empty = empty_count

        # Show real-time video frame in Streamlit
        stframe.image(img_rgb, channels="RGB", use_container_width=True)

    cap.release()

    # Show final results after the video ends
    st.write("✅ **Final Parking Status After Video**")
    st.write(f"🔹 **Total Slots:** {total_slots}")
    st.write(f"🔴 **Final Occupied Slots:** {final_occupied}")
    st.write(f"🟢 **Final Empty Slots:** {final_empty}")

# ========== MAIN STREAMLIT APP ==========
def main():
    st.title("🚗 Parking Lot Detection - Video Processing🚗")
    st.subheader("Upload Parking Lot Video🎥")
    uploaded_file = st.file_uploader("📂 Choose a video", type=["mp4", "avi", "mov"])

    if st.button("To Process Image📷"):
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/admin/stream_img.py"])

    if uploaded_file is not None:
        save_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ File saved: {save_path}")

        # Process video and detect parking status dynamically
        process_video(save_path)

    if st.button("Logout"):
        subprocess.Popen(["streamlit", "run", "D:/project_finalize/main2.py"])

if __name__ == '__main__':
    main()
