import pandas as pd
import yfinance as yf


def get_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return pd.DataFrame()


def get_us_tickers(include_exchanges=("nasdaq", "nyse")) -> pd.DataFrame:
    exchange_urls = {
        "nasdaq": "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt",
        "nyse": "ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt",
    }

    frames = []
    for exch in include_exchanges:
        if exch not in exchange_urls:
            raise ValueError(
                f"Unknown exchange '{exch}'. Valid: {list(exchange_urls.keys())}"
            )
        try:
            df = pd.read_csv(exchange_urls[exch], sep="|")
            frames.append(df)
        except Exception as e:
            print(f"⚠️ Failed to fetch {exch.upper()} tickers: {e}")

    if not frames:
        raise RuntimeError("No ticker data fetched from any exchange.")

    tickers = pd.concat(frames, ignore_index=True)
    # Keep only relevant columns
    cols = [
        c
        for c in ["Symbol", "Security Name", "Exchange", "ETF", "Market Category"]
        if c in tickers.columns
    ]
    tickers = tickers[cols]

    return tickers


tickers = get_us_tickers()
print(tickers.head())
print(tickers.shape)
