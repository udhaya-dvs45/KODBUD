# app.py
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
from tensorflow import keras
import cv2

# -------------------------------
# 1️⃣ Load Saved Model
# -------------------------------
model = keras.models.load_model(r"C:\Users\Udhaya kiran\OneDrive\Desktop\KODBUD\TASK-4\mnist_cnn_model.h5")

st.title("🖌️ Handwritten Digit Recognizer")
st.write("Draw a digit (0-9) below or upload an image, and the model will predict it.")

# -------------------------------
# 2️⃣ Draw Digit Using Streamlit Canvas
# -------------------------------
st.write("## Draw your digit below:")

# Create a white canvas
canvas_size = 280  # 10x MNIST size for better drawing
canvas = np.ones((canvas_size, canvas_size), dtype=np.uint8) * 255

# Use Streamlit's built-in file uploader for now (later can add st_canvas)
uploaded_file = st.file_uploader("Or upload an image...", type=["png", "jpg", "jpeg"])

img_to_predict = None

# -------------------------------
# 3️⃣ Process Uploaded Image
# -------------------------------
if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('L')       # grayscale
    img = ImageOps.invert(img)                         # invert colors if needed
    img = img.resize((28,28))
    img_to_predict = np.array(img)

# -------------------------------
# 4️⃣ Predict Button
# -------------------------------
if st.button("Predict"):
    if img_to_predict is not None:
        # Normalize
        img_array = img_to_predict / 255.0
        img_array = img_array.reshape(1,28,28,1)

        prediction = model.predict(img_array)
        predicted_digit = np.argmax(prediction)

        st.image(img_to_predict, caption='Input Digit', width=100)
        st.write(f"### Predicted Digit: {predicted_digit}")
    else:
        st.write("Please draw or upload a digit first!")
