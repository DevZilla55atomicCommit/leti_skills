---
name: visual-analysis-plotting
description: Standards for identifying, processing, and visualizing finance data using yfinance and Plotly.
tags: [forex, plotting, python, yfinance]
---

# Visual Analytics Reporting & Charting

This skill defines the standards for creating high-fidelity, interactive charts within the **Forex Center**, converting raw market data into professional-grade reports.

## 📊 Technical Standards
All charts must be rendered as **Interactive HTML** files stored in `/Reporting/Charts`.

### Required Plotting Specs:
1.  **Advanced Candlestick Charts:** For visualizing price action (Open, High, Low, Close). Use standard Bullish (Green) and Bearish (Red) palettes.
2.  **RS Index Overlay:** A secondary Y-axis line graph with a 70 (Overbought) / 30 (Oversold) threshold band for identifying clear resistance/support levels.
3.  **Volume Bar Graphs:** Vertical bars at the bottom of the chart to correlate liquidity spikes with price movement.

## 🛠 Implementation Architecture (Python + Plotly)

### Data Acquisition & Processing
We utilize **yfinance** for data retrieval, but because it often returns MultiIndex columns even for single-ticker requests, we must flatten the result before processing:

```python
import yfinance as yf
import pandas as pd

def get_clean_data(symbol, period="1d", interval="1m"):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    
    if df.empty:
        return None
    
    # Standardize MultiIndex columns (Fix for concurrent/multiple requests)
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs(symbol, axis=1, level=0) if symbol in df.columns.values else df
        
    return df
```

### Indicators Module
Use the following standard helper functions:
- **EMA:** `series.ewm(span=period, adjust=False).mean()`
- **RSI:** Standarded 14-day relative strength calculation.

## 📂 Reporting Workflow
Each analysis scan must follow this execution flow:
1.  **Fetch:** Pull via `yfinance`.
2.  **Analyze:** Execute Technical Indicator calculations (Analysis Engine).
3.  **Visualize:** Pass the resulting data into a Plotly multi-subplot constructor (`make_subplots`).
4.  **Store:** Save as `.html` in the local vault path.

# Pitfalls encountered:
- MultiIndex Error: Always check `isinstance(df.columns, pd.MultiIndex)` before accessing columns like 'Close'.
- Numeric Casting: Ensure all price/volume columns are explicitly cast to `pd.to_numeric` to avoid string concatenation errors during indicator calculation.
- Division by Zero: In RSI/Indicators, replace zeros in denominators with 1 to prevent `Inf`/`NaN` labels on the charts.
- **Flat Cast Enforcement:** When extracting data for Plotly (especially when processing multiple symbols), ensure values are converted to a flat list via `.values.flatten()` before calling `pd.to_numeric`. This prevents `TypeError` where `pandas` receives a DataFrame/Series instead of a 1D array in the plotting constructor.
