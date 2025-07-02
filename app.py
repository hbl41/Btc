import streamlit as st
import datetime
import yfinance as yf

st.title("Bitcoin DCA Simulator")

# ---- Widgets ---------------------------------------------------------------
daily = st.slider("Daily USD investment", 1, 100, 10)
start = st.date_input("Start date", datetime.date(2022, 1, 1))
end   = datetime.date(2025, 7, 1)

# ---- Data loader -----------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_btc_history(start_date, end_date):
    try:
        df = yf.download(
            "BTC-USD",
            start=start_date,
            end=end_date + datetime.timedelta(days=1),
            progress=False,
            threads=False,   # avoid some Cloud timeouts
        )
        prices = df["Close"].dropna()
        if prices.empty:
            raise ValueError("Price data empty")
        return prices
    except Exception as err:
        # Catch network/HTTP errors from yfinance (requests) or empty data
        st.error(f"⚠️  Could not fetch BTC prices: {err}")
        return None

prices = load_btc_history(start, end)
if prices is None:
    st.stop()

# ---- DCA math --------------------------------------------------------------
btc    = (daily / prices).sum()
spent  = daily * len(prices)
value  = btc * prices.iloc[-1]

# ---- Display ---------------------------------------------------------------
st.metric("BTC accumulated", f"{btc:.5f}")
st.metric("Total invested",  f"${spent:,.0f}")
st.metric(f"Value on {end}", f"${value:,.0f}")

cumulative_btc = (daily / prices).cumsum()
portfolio_val  = cumulative_btc * prices
st.line_chart(portfolio_val)
