import streamlit as st
import datetime
import pandas as pd

st.title("Bitcoin DCA Simulator")

# ── Load static BTC price data ────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_prices() -> pd.Series:
    df = pd.read_csv("btc_prices.csv", parse_dates=["Date"])
    df = df[["Date", "Close"]].dropna()
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna().sort_values("Date")
    return df.set_index("Date")["Close"]

prices_all = load_prices()

# ── Input controls ────────────────────────────────────────────────────────────
daily = st.slider("Daily USD investment", 1, 100, 10)

min_date = prices_all.index.min().date()
max_date = datetime.date(2025, 7, 1)
start = st.date_input(
    "Start date",
    max(min_date, datetime.date(2022, 1, 1)),
    min_value=min_date,
    max_value=max_date,
)
end = max_date

# ── Slice and clean price data ────────────────────────────────────────────────
mask = (prices_all.index >= pd.Timestamp(start)) & (prices_all.index <= pd.Timestamp(end))
prices = prices_all.loc[mask].dropna()

if prices.empty:
    st.error("No price data found for selected date range.")
    st.stop()

# ── DCA calculations ─────────────────────────────────────────────────────────
daily_float = float(daily)  # ensure float division
btc = (daily_float / prices).sum()
spent = daily_float * len(prices)
value = btc * prices.iloc[-1]

# ── Display metrics ──────────────────────────────────────────────────────────
st.metric("BTC accumulated", f"{btc:.5f}")
st.metric("Total invested", f"${spent:,.0f}")
st.metric(f"Value on {end}", f"${value:,.0f}")

# ── Portfolio growth chart ───────────────────────────────────────────────────
cumulative_btc = (daily_float / prices).cumsum()
portfolio_value = cumulative_btc * prices
st.line_chart(portfolio_value)
