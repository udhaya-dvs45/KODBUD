# train_mnist.py

import tensorflow as tf
from tensorflow import keras
import numpy as np

# -------------------------------
# 1️⃣ Load MNIST Dataset
# -------------------------------
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

# Normalize pixel values
X_train = X_train / 255.0
X_test = X_test / 255.0

# Reshape for CNN: (samples, height, width, channels)
X_train = X_train.reshape(-1,28,28,1)
X_test = X_test.reshape(-1,28,28,1)

# -------------------------------
# 2️⃣ Build CNN Model
# -------------------------------
model = keras.Sequential([
    keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(64, (3,3), activation='relu'),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# -------------------------------
# 3️⃣ Compile the Model
# -------------------------------
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# -------------------------------
# 4️⃣ Train the Model
# -------------------------------
model.fit(X_train, y_train, epochs=5, validation_split=0.1)

# -------------------------------
# 5️⃣ Evaluate on Test Set
# -------------------------------
test_loss, test_acc = model.evaluate(X_test, y_test)
print("Test Accuracy:", test_acc)

# -------------------------------
# 6️⃣ Save the Model
# -------------------------------
model.save("mnist_cnn_model.h5")
print("Model saved as mnist_cnn_model.h5")
