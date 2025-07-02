import streamlit as st
import datetime
import pandas as pd

st.title("Bitcoin DCA Simulator")

# ── Load static price data ────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_prices() -> pd.Series:
    df = pd.read_csv("btc_prices.csv", parse_dates=["Date"])
    if df.empty:
        raise ValueError("btc_prices.csv is empty – run prepare_data.py first.")
    return df.set_index("Date")["Close"].sort_index()   # ensure ascending

prices_all = load_prices()

# ── Widgets ───────────────────────────────────────────────────────────────────
daily = st.slider("Daily USD investment", 1, 100, 10)

min_date = prices_all.index.min().date()               # earliest date in CSV
max_date = datetime.date(2025, 7, 1)                   # fixed end of DCA period
start = st.date_input(
    "Start date",
    max(min_date, datetime.date(2022, 1, 1)),
    min_value=min_date,
    max_value=max_date,
)
end = max_date

# ── Slice chosen period safely ────────────────────────────────────────────────
start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
mask   = (prices_all.index >= start_ts) & (prices_all.index <= end_ts)
prices = prices_all.loc[mask]

if prices.empty:
    st.error("No price data in the chosen range.")
    st.stop()

# ── DCA calculations ─────────────────────────────────────────────────────────
btc    = (daily / prices).sum()
spent  = daily * len(prices)
value  = btc * prices.iloc[-1]

# ── Display metrics ──────────────────────────────────────────────────────────
st.metric("BTC accumulated", f"{btc:.5f}")
st.metric("Total invested",  f"${spent:,.0f}")
st.metric(f"Value on {end}", f"${value:,.0f}")

# ── Portfolio-value chart ────────────────────────────────────────────────────
cumulative_btc  = (daily / prices).cumsum()
portfolio_value = cumulative_btc * prices
st.line_chart(portfolio_value)
