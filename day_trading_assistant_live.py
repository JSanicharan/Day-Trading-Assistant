import yfinance as yf
import pandas as pd
import numpy as np

# ------------------ Trend Module ------------------
def get_trend_bias(df_1h):
    """
    Determines trend bias based on 20-period SMA.
    Returns 'bullish', 'bearish', or None if insufficient data.
    """
    if df_1h.empty or len(df_1h) < 20:
        return None

    df_1h = df_1h.copy()
    df_1h['SMA20'] = df_1h['Close'].rolling(20, min_periods=20).mean()

    last_close = df_1h['Close'].iloc[-1].item()
    last_sma = df_1h['SMA20'].iloc[-1].item()

    if pd.isna(last_sma):
        return None

    return "bullish" if last_close > last_sma else "bearish"

# ------------------ FVG Module ------------------
def find_fvg(df_15, bias, min_gap_pct=0.0005, min_gap_dollar=0.1):
    """
    Finds Fair Value Gaps (FVG) in 15-min bars based on trend bias.
    Returns a list of detected setups with entry, stop, target.
    """
    fvgs = []

    df_15 = df_15.copy()
    for i in range(2, len(df_15)):
        try:
            high1, low1 = df_15['High'].iloc[i-2].item(), df_15['Low'].iloc[i-2].item()
            high3, low3 = df_15['High'].iloc[i].item(), df_15['Low'].iloc[i].item()
            close_now = df_15['Close'].iloc[i].item()
        except Exception:
            continue

        # Bullish FVG
        if bias == "bullish" and low3 > high1:
            gap_dollar = low3 - high1
            gap_pct = gap_dollar / close_now
            if gap_dollar >= min_gap_dollar and gap_pct >= min_gap_pct:
                entry = high1
                stop = low1
                target = entry + 1.5 * gap_dollar
                fvgs.append({
                    "type": "bullish",
                    "entry": round(entry,2),
                    "stop": round(stop,2),
                    "target": round(target,2),
                    "time": df_15.index[i]
                })

        # Bearish FVG
        if bias == "bearish" and high3 < low1:
            gap_dollar = low1 - high3
            gap_pct = gap_dollar / close_now
            if gap_dollar >= min_gap_dollar and gap_pct >= min_gap_pct:
                entry = low1
                stop = high1
                target = entry - 1.5 * gap_dollar
                fvgs.append({
                    "type": "bearish",
                    "entry": round(entry,2),
                    "stop": round(stop,2),
                    "target": round(target,2),
                    "time": df_15.index[i]
                })

    return fvgs

# ------------------ Historical Analysis ------------------
def analyze_results(results):
    all_fvgs = []
    for ticker, data in results.items():
        fvgs = data['fvgs']
        all_fvgs.extend(fvgs)
        total_trades = len(fvgs)
        print(f"\n=== {ticker} Analysis ===")
        print(f"Trend Bias: {data['bias']}")
        print(f"Total FVGs detected: {total_trades}")

    # Top 10 largest gaps across all tickers
    ranked = sorted(all_fvgs, key=lambda x: abs(x['target'] - x['entry']), reverse=True)
    print("\n=== Top Ranked Setups Across All Tickers ===")
    for f in ranked[:10]:
        print(f"{f['type']} | Entry: {f['entry']} | Stop: {f['stop']} | Target: {f['target']} | Time: {f['time']}")

# ------------------ Near-Live Signal Scanner ------------------
def live_signals(tickers, recent_bars=50):
    """
    Simulates real-time scanning for Fair Value Gaps on the most recent bars.
    Prints actionable entries, stops, and targets.
    """
    print("\n=== Checking Live Signals ===")
    for ticker in tickers:
        try:
            df_1h = yf.download(ticker, period="5d", interval="1h", progress=False)
            df_15 = yf.download(ticker, period="2d", interval="15m", progress=False)

            if df_1h.empty or df_15.empty:
                print(f"No data for {ticker}, skipping...")
                continue

            df_1h = df_1h.copy()
            df_15 = df_15.copy()
            df_15.attrs['ticker'] = ticker

            bias = get_trend_bias(df_1h)
            if bias is None:
                print(f"{ticker}: Not enough data to determine trend, skipping...")
                continue

            recent_df = df_15.tail(recent_bars)
            fvgs = find_fvg(recent_df, bias)

            if fvgs:
                print(f"\n{ticker} | Trend: {bias} | Potential Trades:")
                for f in fvgs:
                    print(f"{f['type']} | Entry: {f['entry']} | Stop: {f['stop']} | Target: {f['target']} | Time: {f['time']}")
            else:
                print(f"{ticker}: No signals found in recent bars.")

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

# ------------------ Main Execution ------------------
def main():
    tickers = ["AAPL","MSFT","NVDA","AMD","GOOG","SPY","QQQ","AMZN","TSLA"]

    # Historical analysis
    print("=== Running Historical Analysis ===")
    results = {}
    for ticker in tickers:
        try:
            df_1h = yf.download(ticker, period="60d", interval="1h", progress=False)
            df_15 = yf.download(ticker, period="60d", interval="15m", progress=False)

            if df_1h.empty or df_15.empty:
                continue

            df_1h = df_1h.copy()
            df_15 = df_15.copy()
            df_15.attrs['ticker'] = ticker

            bias = get_trend_bias(df_1h)
            if bias is None:
                continue

            fvgs = find_fvg(df_15, bias)
            results[ticker] = {"bias": bias, "fvgs": fvgs}
            print(f"{ticker}: {len(fvgs)} historical FVG(s) detected | Trend: {bias}")

        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")

    analyze_results(results)

    # Near-live signals
    live_signals(tickers)

# ------------------ Run ------------------
if __name__ == "__main__":
    main()
