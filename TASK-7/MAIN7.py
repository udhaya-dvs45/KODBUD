import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# --- UI Setup ---
st.set_page_config(page_title="LSTM Stock Predictor", page_icon="🤖")
st.title("🤖 LSTM Stock Price Predictor")
ticker = st.text_input("Enter Ticker (e.g., TSLA, GOOGL)", "AAPL")

# --- Load Data ---
@st.cache_data
def load_data(symbol):
    data = yf.download(symbol, start="2020-01-01")
    return data

df = load_data(ticker)

if not df.empty:
    st.subheader(f"Historical Close Price for {ticker}")
    st.line_chart(df['Close'])

    # --- Preprocessing ---
    # LSTM needs data scaled between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['Close']])

    # Create sequences (Looking back 60 days to predict the next day)
    prediction_days = 60
    x_train, y_train = [], []

    for i in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[i-prediction_days:i, 0])
        y_train.append(scaled_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # --- Build LSTM Model ---
    if st.button("Train & Predict"):
        with st.spinner('Training the LSTM Brain... this may take a minute.'):
            model = Sequential([
                LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
                Dropout(0.2),
                LSTM(units=50, return_sequences=False),
                Dropout(0.2),
                Dense(units=25),
                Dense(units=1)
            ])

            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=0)

            # --- Prediction ---
            # Get the last 60 days to predict tomorrow
            real_data = [scaled_data[len(scaled_data) - prediction_days:len(scaled_data), 0]]
            real_data = np.array(real_data)
            real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

            prediction = model.predict(real_data)
            prediction = scaler.inverse_transform(prediction) # Undo scaling

            # --- Results ---
            current_price = df['Close'].iloc[-1].values[0]
            predicted_price = prediction[0][0]
            
            st.divider()
            col1, col2 = st.columns(2)
            col1.metric("Latest Price", f"${current_price:.2f}")
            col2.metric("LSTM Predicted Price", f"${predicted_price:.2f}", 
                        f"{predicted_price - current_price:.2f}")

            # Simple Visualization
            st.success("The model has finished processing the time-series patterns.")
else:
    st.error("Invalid Ticker.")