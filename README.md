# Real-Time Stock Market Dashboard

A Streamlit-based dashboard to monitor real-time stock prices, explore historical trends, forecast future prices using **Prophet**, and analyze news sentiment using **TextBlob**.

✅ **Features:**
- Select from a curated list of US and Indian stocks
- Live price metrics (current price, high/low, volume)
- Interactive charts: line chart and candlestick chart (Plotly)
- Historical data table
- **AI-powered forecast** (30-day) using Prophet
- **News sentiment analysis** via Yahoo Finance news + TextBlob

---

## 🧰 Requirements

This project is built with Python and requires the packages listed in `requirements.txt`.

### Recommended setup (Python 3.10+)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

> Note: If you run into issues installing `prophet`, make sure you have a supported compiler/runtime for your platform. On Windows, it is often easiest to install `prophet` via `pip` once the build tools are available.

---

## ▶️ Running the Dashboard

From the project root:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

---

## 🔍 What You Can Do

- Choose a stock from the sidebar (US or India).
- Select a historical time period (1 day → Max).
- View live metrics (price, highs/lows, volume).
- Explore interactive charts and historical data.
- Generate a 30-day forecast (Prophet model) and view confidence bands.
- Read recent news headlines and see sentiment breakdown.

---

## 🧩 Project Structure

- `app.py` – Main Streamlit app.
- `requirements.txt` – Python dependencies.

---

## ⚙️ Customization Ideas

- Add support for custom ticker symbols.
- Improve prediction accuracy (more advanced models / tuning).
- Add caching for news sentiment to reduce repeated web requests.
- Allow switching between data sources (e.g., Alpha Vantage, Finnhub).

---

## 🧠 Notes

- This dashboard uses Yahoo Finance via `yfinance` for market data.
- News sentiment is derived from article headlines and may not reflect full sentiment.
- Forecasts are for educational/demo purposes; do not treat them as investment advice.

---

Made with ❤️ using Streamlit, Plotly, Prophet, and TextBlob.
