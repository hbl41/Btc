import yfinance as yf
import pandas as pd

START = "2022-01-01"
END   = "2025-07-02"         # end is exclusive, so +1 day for 2025-07-01

df = yf.download(
    "BTC-USD",
    start=START,
    end=END,
    progress=False,
    threads=False,           # avoids some Cloud timeouts
)
if df.empty:
    raise RuntimeError("Download failed; try again later.")

# Keep only Date and Close, save to CSV
df.reset_index()[["Date", "Close"]].to_csv("btc_prices.csv", index=False)
print(f"Saved btc_prices.csv with {len(df)} rows.")
