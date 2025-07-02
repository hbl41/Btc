import streamlit as st
import datetime
import pandas as pd

st.title("Bitcoin DCA Simulator")

# --- Load static price data ---------------------------------
@st.cache_data(show_spinner=False)
def load_prices():
    df = pd.read_csv("btc_prices.csv", parse_dates=["Date"])
    return df.set_index("Date")["Close"].dropna()

prices_all = load_prices()
if prices_all.empty:
    st.error("btc_prices.csv missing or empty – run prepare_data.py first.")
    st.stop()

# --- Inputs -------------------------------------------------
daily = st.slider("Daily USD investment", 1, 100, 10)

min_date = prices_all.index.min().date()
default_start = max(datetime.date(2022, 1, 1), min_date)
start = st.date_input(
    "Start date",
    default_start,
    min_value=min_date,
    max_value=datetime.date(2025, 7, 1),
)
end = datetime.date(2025, 7, 1)

# --- Slice data to chosen range -----------------------------
prices = prices_all.loc[start:end]
if prices.empty:
    st.error("No price data in chosen range.")
    st.stop()

# --- DCA calculations ---------------------------------------
btc    = (daily / prices).sum()
spent  = daily * len(prices)
value  = btc * prices.iloc[-1]

# --- Display metrics ----------------------------------------
st.metric("BTC accumulated", f"{btc:.5f}")
st.metric("Total invested",  f"${spent:,.0f}")
st.metric(f"Value on {end}", f"${value:,.0f}")

# --- Chart portfolio value ----------------------------------
cumulative_btc  = (daily / prices).cumsum()
portfolio_value = cumulative_btc * prices
st.line_chart(portfolio_value)
