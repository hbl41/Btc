import streamlit as st, datetime, yfinance as yf

st.title("Bitcoin DCA Simulator")

daily = st.slider("Daily USD", 1, 100, 10)
start = st.date_input("Start date", datetime.date(2022, 1, 1))
end   = datetime.date(2025, 7, 1)

prices = yf.download("BTC-USD", start, end + datetime.timedelta(days=1))["Close"]
btc    = (daily / prices).sum()
spent  = daily * len(prices)
value  = btc * prices.iloc[-1]

st.metric("BTC accumulated", f"{btc:.5f}")
st.metric("Total invested",  f"${spent:,.0f}")
st.metric(f"Value on {end}", f"${value:,.0f}")

st.line_chart((daily / prices).cumsum() * prices)
