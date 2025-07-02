import streamlit as st
import datetime
import yfinance as yf

st.title("Bitcoin DCA Simulator")

# Input widgets
daily = st.slider("Daily USD investment", 1, 100, 10)
start = st.date_input("Start date", datetime.date(2022, 1, 1))
end = datetime.date(2025, 7, 1)

# Get BTC price data
data = yf.download("BTC-USD", start=start, end=end + datetime.timedelta(days=1))
prices = data["Close"].dropna()

if prices.empty:
    st.error("No price data found for selected date range.")
else:
    # Calculate totals
    btc = (daily / prices).sum()
    spent = daily * len(prices)
    value = btc * prices.iloc[-1]

    # Output metrics
    st.metric("BTC accumulated", f"{btc:.5f}")
    st.metric("Total invested", f"${spent:,.0f}")
    st.metric(f"Value on {end}", f"${value:,.0f}")

    # Chart portfolio value over time
    cumulative_btc = (daily / prices).cumsum()
    portfolio_value = cumulative_btc * prices
    st.line_chart(portfolio_value)
