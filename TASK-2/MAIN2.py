import cv2
import numpy as np
import streamlit as st
from PIL import Image

# Page title
st.title("🙂 Face Detection using OpenCV + Streamlit")

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# Upload image
uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.4,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw rectangle on faces
    for (x, y, w, h) in faces:
        cv2.rectangle(
            image_np,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    # Show results
    st.subheader(f"Detected Faces: {len(faces)}")
    st.image(image_np, channels="BGR", use_column_width=True)
