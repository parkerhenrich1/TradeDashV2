import pandas as pd

nasdaq = pd.read_csv(
    "NASDAQ.csv"
)

# Clean LastSale
nasdaq["LastSale"] = (
    nasdaq["LastSale"]
    .astype(str)
    .str.replace("$", "", regex=False)
)

nasdaq["LastSale"] = pd.to_numeric(
    nasdaq["LastSale"],
    errors="coerce"
)

# Clean MarketCap
nasdaq["MarketCap"] = (
    nasdaq["MarketCap"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace("B", "e9", regex=False)
    .str.replace("M", "e6", regex=False)
    .str.replace(",", "", regex=False)
)

nasdaq["MarketCap"] = pd.to_numeric(
    nasdaq["MarketCap"],
    errors="coerce"
)

filtered = nasdaq[
    (nasdaq["LastSale"] >= 10)
    &
    (nasdaq["MarketCap"] >= 300_000_000)
]

tickers = filtered["Symbol"].tolist()

print(
    f"Universe Size: {len(tickers)}"
)

pd.DataFrame(
    {"Symbol": tickers}
).to_excel(
    "TickerUniverse.xlsx",
    index=False
)

print(
    "TickerUniverse.xlsx created."
)