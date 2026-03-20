import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("📈 AI Stock Price Analysis App")

# Input
stock_name = st.text_input("Enter Stock Name (Example: TATAMOTORS.NS)")

if st.button("Analyze Stock"):

    # Create ticker object
    stock = yf.Ticker(stock_name)

    # 📍 REAL-TIME PRICE
    try:
        current_price = stock.history(period="1d")['Close'][-1]
    except:
        st.error("❌ Unable to fetch stock data. Check stock name.")
        st.stop()

    # 📊 Historical data
    data = stock.history(start="2020-01-01", end="2025-01-01")

    if data.empty:
        st.error("❌ Invalid stock name")
    else:
        data = data[['Close']].dropna()

        # 📊 Moving Averages
        data['MA50'] = data['Close'].rolling(window=50).mean()
        data['MA200'] = data['Close'].rolling(window=200).mean()

        ma50 = data['MA50'].iloc[-1]
        ma200 = data['MA200'].iloc[-1]

        # 📈 Graph
        st.subheader("📈 Price Trend with Moving Averages")
        fig, ax = plt.subplots()
        ax.plot(data['Close'], label="Close Price")
        ax.plot(data['MA50'], label="MA50")
        ax.plot(data['MA200'], label="MA200")
        ax.legend()
        st.pyplot(fig)

        # 📊 Analysis Logic

        # Predicted price (stable)
        predicted_price = ma50

        # Status
        if current_price > ma50:
            status = "Slightly Overpriced"
        else:
            status = "Undervalued"

        # Trend
        if ma50 > ma200:
            trend = "UPWARD 📈"
        else:
            trend = "DOWNWARD 📉"

        # Percentage change
        percent = ((predicted_price - current_price) / current_price) * 100

        # Buy/Sell range
        buy_price = ma50 * 0.97
        sell_price = ma50 * 1.05

        # 📊 Output
        st.subheader("📊 Analysis Result")

        st.write(f"📍 **Live Price:** ₹{round(current_price,2)}")
        st.write(f"📊 **50-Day Avg (Fair Value):** ₹{round(ma50,2)}")
        st.write(f"📊 **200-Day Avg:** ₹{round(ma200,2)}")

        st.write(f"📊 **Status:** {status}")
        st.write(f"📈 **Trend:** {trend}")
        st.write(f"📉 **Expected Change:** {round(percent,2)}%")

        st.write("### 💡 Recommendation")
        st.write(f"Buy Below ₹{round(buy_price,2)}")
        st.write(f"Sell Above ₹{round(sell_price,2)}")
