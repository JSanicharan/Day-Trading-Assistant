# Day Trading Assistant

A Python-based assistant that analyzes stock data, identifies Fair Value Gaps (FVGs), and calculates actionable trade setups with entry, stop-loss, and target levels.

---

## Features

- **Historical Analysis:** Detects bullish and bearish FVGs over the past 60 days using 1-hour and 15-minute bars.  
- **Trend Bias Detection:** Determines overall market trend using a 20-period Simple Moving Average (SMA20).  
- **Near-Live Signals:** Scans the most recent 15-minute bars for potential trade setups.  
- **Trade Setup Calculation:** Automatically calculates entry, stop-loss, and target levels for each detected FVG.  
- **Robust Data Handling:** Gracefully handles missing or ambiguous data to reduce runtime errors.

---

## Requirements

- Python 3.10+  
- pandas >= 2.0  
- numpy >= 1.25  
- yfinance >= 0.2.27  

Install dependencies with:

pip install pandas numpy yfinance

Supported Tickers
By default, the script scans:
AAPL, MSFT, NVDA, AMD, GOOG, SPY, QQQ, AMZN, TSLA
Modify the tickers list in day_trading_assistant_live.py to add or remove symbols.

## Usage
Clone the repository:
git clone <YOUR_REPO_URL>
cd day-trading-assistant

Run the main script:
python day_trading_assistant_live.py

Output includes:
Historical FVG analysis for all tickers.
Top-ranked trade setups across tickers.
Near-live potential trades with entry, stop, and target.

## How It Works
Trend Bias:
 - Uses the last closing price of 1-hour bars and compares it to the 20-period SMA.
 - Determines a bias: bullish if price > SMA, otherwise bearish.

Fair Value Gap (FVG) Detection:
 - Checks 15-minute bars for gaps between high and low of separated bars.
 - Only considers gaps above a minimum dollar value and minimum percentage of current price.
 - Calculates entry, stop, and target for each valid gap.

Historical Analysis:
 - Scans the past 60 days of data for each ticker.
 - Aggregates all FVGs and ranks the top setups by size of gap.

Near-Live Signal Scanner:
 - Analyzes the last 50 15-minute bars in real-time simulation.
 - Prints actionable trade setups with entry, stop, target, and time.

## Notes
 - Trend bias is determined from the last closing price relative to SMA20 on 1-hour bars.
 -  FVG detection uses a minimum gap of 0.1 USD and 0.05% of current price by default.
 - Live scanning uses recent 50 15-minute bars for actionable signals.
 - The script handles missing or ambiguous data to avoid runtime errors.
 - This is not financial advice; use at your own risk.
 - License
 - This project is provided for educational purposes. Use at your own risk.
