import streamlit as st
import os
import cv2
import numpy as np
import sqlite3
from ultralytics import YOLO
from PIL import Image, ImageDraw
import subprocess
import base64

st.set_page_config(page_title="Image Processing", page_icon="📤")

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
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local(r"D:\project_finalize\assets\images.jpeg")

# ✅ Load YOLO model
model = YOLO("yolov8n.pt")

# ✅ Function to detect red areas as empty slots
def detect_red_as_empty(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
    mask = mask1 + mask2
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    empty_slots = [(cv2.boundingRect(cnt)) for cnt in contours]
    return empty_slots

# ✅ Function to process the uploaded image
def process_uploaded_image(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # YOLO Detection for occupied slots
    results = model(image_path)
    detections = results[0].boxes.xyxy.cpu().numpy()
    occupied_slots = [(int(x1), int(y1), int(x2), int(y2)) for x1, y1, x2, y2 in detections]
    
    # Detect Red Regions as Empty Slots
    empty_slots = detect_red_as_empty(img)
    
    # Convert OpenCV image to PIL for annotation
    annotated_img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(annotated_img)
    
    # Draw occupied slots (YOLO)
    for x1, y1, x2, y2 in occupied_slots:
        draw.rectangle([x1, y1, x2, y2], outline="green", width=3)
        draw.text((x1, y1 - 10), "Occupied", fill="green")
    
    # Draw empty slots (Red Regions)
    for x, y, w, h in empty_slots:
        draw.rectangle([x, y, x + w, y + h], outline="blue", width=3)
        draw.text((x, y - 10), "Empty", fill="blue")
    
    img_rgb = np.array(annotated_img)
    st.image(img_rgb, caption="Processed Image with Detections", use_container_width=True)
    
    return len(occupied_slots), len(empty_slots)

# ========== MAIN STREAMLIT APP ==========
st.title("🚗 Parking Lot Detection - Image Processing")
st.subheader("📂 Upload Parking Lot Image 📷")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

if st.button("To Process Video 🎥"):
    subprocess.Popen(["streamlit", "run", "D:/project_finalize/admin/stream_video.py"])

if uploaded_file is not None:
    save_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"✅ File saved: {save_path}")
    
    # Display original image
    st.image(save_path, caption="Uploaded Image", use_container_width=True)
    
    # Process Image
    auto_occupied, auto_empty = process_uploaded_image(save_path)
    
    st.markdown(f"""
    <h2 style=' color: white;'>🔹 Total Slots: {auto_occupied + auto_empty}</h2>
    <h2 style=' color: white;'>🔹 Occupied Slots (YOLO-detected): {auto_occupied}</h2>
    <h2 style=' color: white;'>🔹 Empty Slots (Red Regions): {auto_empty}</h2>

    """,
    unsafe_allow_html=True)

# ✅ Logout Button
if st.button("Logout"):
    subprocess.Popen(["streamlit", "run", "D:/project_finalize/main2.py"])
