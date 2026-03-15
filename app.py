import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
from prophet import Prophet
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import re

# Page configuration
st.set_page_config(
    page_title="Real-Time Stock Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Global ── */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Page / main background ── */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important;
    }
    [data-testid="stHeader"] {
        background-color: #0F172A !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] label {
        color: #94A3B8 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* ── Title & body text ── */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-family: 'Inter', sans-serif !important;
    }
    p, span, li, div {
        color: #CBD5E1 !important;
    }
    .stMarkdown p {
        color: #94A3B8 !important;
    }

    /* ── Tabs ── */
    [data-testid="stTabs"] [role="tab"] {
        color: #94A3B8 !important;
        font-weight: 500;
        font-size: 0.9rem;
        background: transparent;
        border-bottom: 2px solid transparent;
        padding: 8px 16px;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: #10B981 !important;
        border-bottom: 2px solid #10B981 !important;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-left: 3px solid #10B981 !important;
        padding: 18px 22px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35) !important;
    }

    /* Metric LABEL */
    [data-testid="stMetricLabel"] > div,
    [data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }

    /* Metric VALUE */
    [data-testid="stMetricValue"] > div,
    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }

    /* Metric DELTA — gain / loss colours */
    [data-testid="stMetricDelta"][data-direction="up"] > div {
        color: #10B981 !important;
    }
    [data-testid="stMetricDelta"][data-direction="down"] > div {
        color: #F87171 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.88rem !important;
        font-weight: 500 !important;
    }

    /* ── Dataframe / table ── */
    [data-testid="stDataFrame"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    /* ── Expander (news) ── */
    [data-testid="stExpander"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    [data-testid="stExpander"] summary {
        color: #F8FAFC !important;
    }

    /* ── Divider ── */
    hr {
        border-color: #334155 !important;
    }

    /* ── Spinner / info text ── */
    .stSpinner > div > div {
        border-top-color: #10B981 !important;
    }

    /* ── Selectbox / dropdown inputs ── */
    /* The visible input box */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #0F172A !important;
        border-color: #334155 !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
    }
    /* The selected text inside the box */
    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] [class*="singleValue"],
    [data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #F8FAFC !important;
    }
    /* Dropdown menu list */
    [data-baseweb="popover"] ul,
    [data-baseweb="menu"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
    }
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] [role="option"] {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
    }
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [role="option"]:hover {
        background-color: #334155 !important;
    }
    /* Arrow icon in selectbox */
    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #94A3B8 !important;
    }

    /* ── Inline code (backtick) in sidebar About text ── */
    [data-testid="stSidebar"] code,
    [data-testid="stSidebar"] .stMarkdown code {
        background-color: #334155 !important;
        color: #10B981 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-size: 0.82rem !important;
    }

    /* ── General inline code elsewhere ── */
    .stMarkdown code {
        background-color: #1E293B !important;
        color: #10B981 !important;
        border: 1px solid #334155 !important;
        padding: 1px 5px !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Real-Time Stock Market Dashboard")
st.markdown("Monitor live stock prices, analyze market trends, and make informed investment decisions.")

# Sidebar for user input
st.sidebar.header("User Input")

# Dictionary of popular stocks (US + Indian)
STOCK_SYMBOLS = {
    # ── US Tech ──────────────────────────────────────────────────
    'Apple (AAPL)': 'AAPL',
    'Microsoft (MSFT)': 'MSFT',
    'NVIDIA (NVDA)': 'NVDA',
    'Alphabet / Google (GOOGL)': 'GOOGL',
    'Amazon (AMZN)': 'AMZN',
    'Meta Platforms (META)': 'META',
    'Tesla (TSLA)': 'TSLA',
    'Broadcom (AVGO)': 'AVGO',
    'Oracle (ORCL)': 'ORCL',
    'Salesforce (CRM)': 'CRM',
    'Adobe (ADBE)': 'ADBE',
    'Intel (INTC)': 'INTC',
    'Advanced Micro Devices (AMD)': 'AMD',
    'Qualcomm (QCOM)': 'QCOM',
    'Texas Instruments (TXN)': 'TXN',
    'Applied Materials (AMAT)': 'AMAT',
    'Micron Technology (MU)': 'MU',
    'Cisco Systems (CSCO)': 'CSCO',
    'IBM (IBM)': 'IBM',
    'Palantir (PLTR)': 'PLTR',
    'Snowflake (SNOW)': 'SNOW',
    'Datadog (DDOG)': 'DDOG',
    'ServiceNow (NOW)': 'NOW',
    'Workday (WDAY)': 'WDAY',
    'Palo Alto Networks (PANW)': 'PANW',
    'CrowdStrike (CRWD)': 'CRWD',
    'Fortinet (FTNT)': 'FTNT',
    'Zoom Video (ZM)': 'ZM',
    'Shopify (SHOP)': 'SHOP',
    'Block / Square (SQ)': 'SQ',
    'Spotify (SPOT)': 'SPOT',
    'Netflix (NFLX)': 'NFLX',
    'Uber (UBER)': 'UBER',
    'Airbnb (ABNB)': 'ABNB',
    'DoorDash (DASH)': 'DASH',
    'Lyft (LYFT)': 'LYFT',
    'Snap (SNAP)': 'SNAP',
    'Pinterest (PINS)': 'PINS',
    'Twitter / X (X)': 'X',
    'Roblox (RBLX)': 'RBLX',
    'Unity Software (U)': 'U',
    # ── US Finance ───────────────────────────────────────────────
    'JPMorgan Chase (JPM)': 'JPM',
    'Goldman Sachs (GS)': 'GS',
    'Morgan Stanley (MS)': 'MS',
    'Bank of America (BAC)': 'BAC',
    'Wells Fargo (WFC)': 'WFC',
    'Citigroup (C)': 'C',
    'American Express (AXP)': 'AXP',
    'Visa (V)': 'V',
    'Mastercard (MA)': 'MA',
    'PayPal (PYPL)': 'PYPL',
    'BlackRock (BLK)': 'BLK',
    'Charles Schwab (SCHW)': 'SCHW',
    'Berkshire Hathaway B (BRK-B)': 'BRK-B',
    # ── US Healthcare ─────────────────────────────────────────────
    'Johnson & Johnson (JNJ)': 'JNJ',
    'Pfizer (PFE)': 'PFE',
    'Moderna (MRNA)': 'MRNA',
    'Merck (MRK)': 'MRK',
    'AbbVie (ABBV)': 'ABBV',
    'Eli Lilly (LLY)': 'LLY',
    'Bristol-Myers Squibb (BMY)': 'BMY',
    'UnitedHealth Group (UNH)': 'UNH',
    'CVS Health (CVS)': 'CVS',
    'Thermo Fisher (TMO)': 'TMO',
    # ── US Consumer / Retail ──────────────────────────────────────
    'Walmart (WMT)': 'WMT',
    'Target (TGT)': 'TGT',
    'Costco (COST)': 'COST',
    'Home Depot (HD)': 'HD',
    "Lowe's (LOW)": 'LOW',
    'McDonald\'s (MCD)': 'MCD',
    'Starbucks (SBUX)': 'SBUX',
    'Nike (NKE)': 'NKE',
    'Coca-Cola (KO)': 'KO',
    'PepsiCo (PEP)': 'PEP',
    'Procter & Gamble (PG)': 'PG',
    'Colgate-Palmolive (CL)': 'CL',
    # ── US Energy ─────────────────────────────────────────────────
    'ExxonMobil (XOM)': 'XOM',
    'Chevron (CVX)': 'CVX',
    'ConocoPhillips (COP)': 'COP',
    'NextEra Energy (NEE)': 'NEE',
    # ── US Industrials / Other ────────────────────────────────────
    'Boeing (BA)': 'BA',
    'Caterpillar (CAT)': 'CAT',
    '3M (MMM)': 'MMM',
    'General Electric (GE)': 'GE',
    'Honeywell (HON)': 'HON',
    'Lockheed Martin (LMT)': 'LMT',
    'Raytheon (RTX)': 'RTX',
    'Union Pacific (UNP)': 'UNP',
    'FedEx (FDX)': 'FDX',
    'UPS (UPS)': 'UPS',
    'Eaton (ETN)': 'ETN',
    'S&P 500 ETF (SPY)': 'SPY',
    'Nasdaq 100 ETF (QQQ)': 'QQQ',
    # ── India – Large Cap (NSE) ───────────────────────────────────
    'Reliance Industries': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'Infosys': 'INFY.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Axis Bank': 'AXISBANK.NS',
    'State Bank of India': 'SBIN.NS',
    'Bajaj Finance': 'BAJFINANCE.NS',
    'Bajaj Finserv': 'BAJAJFINSV.NS',
    'Wipro': 'WIPRO.NS',
    'HCL Technologies': 'HCLTECH.NS',
    'Tech Mahindra': 'TECHM.NS',
    'LTIMindtree': 'LTIM.NS',
    'Larsen & Toubro': 'LT.NS',
    'Maruti Suzuki': 'MARUTI.NS',
    'Tata Motors': 'TATAMOTORS.NS',
    'Mahindra & Mahindra': 'M&M.NS',
    'Hero MotoCorp': 'HEROMOTOCO.NS',
    'Bajaj Auto': 'BAJAJ-AUTO.NS',
    'Asian Paints': 'ASIANPAINT.NS',
    'Nestle India': 'NESTLEIND.NS',
    'Hindustan Unilever': 'HINDUNILVR.NS',
    'ITC': 'ITC.NS',
    'Britannia Industries': 'BRITANNIA.NS',
    'Sun Pharmaceutical': 'SUNPHARMA.NS',
    'Dr. Reddy\'s Lab': 'DRREDDY.NS',
    'Cipla': 'CIPLA.NS',
    'Divis Laboratories': 'DIVISLAB.NS',
    'ONGC': 'ONGC.NS',
    'Coal India': 'COALINDIA.NS',
    'NTPC': 'NTPC.NS',
    'Power Grid': 'POWERGRID.NS',
    'Adani Ports': 'ADANIPORTS.NS',
    'Adani Enterprises': 'ADANIENT.NS',
    'Adani Green Energy': 'ADANIGREEN.NS',
    'Tata Steel': 'TATASTEEL.NS',
    'JSW Steel': 'JSWSTEEL.NS',
    'Hindalco': 'HINDALCO.NS',
    'UltraTech Cement': 'ULTRACEMCO.NS',
    'Grasim Industries': 'GRASIM.NS',
    'Titan Company': 'TITAN.NS',
    'Zomato': 'ZOMATO.NS',
    'Nykaa (FSN E-Commerce)': 'NYKAA.NS',
    'Paytm (One97 Comm.)': 'PAYTM.NS',
    'Delhivery': 'DELHIVERY.NS',
    'Havells India': 'HAVELLS.NS',
    'Siemens India': 'SIEMENS.NS',
    'ABB India': 'ABB.NS',
    'Pidilite Industries': 'PIDILITIND.NS',
    'Berger Paints': 'BERGEPAINT.NS',
    'Godrej Consumer': 'GODREJCP.NS',
    'Dabur India': 'DABUR.NS',
    'Marico': 'MARICO.NS',
    'Colgate India': 'COLPAL.NS',
    'Persistent Systems': 'PERSISTENT.NS',
    'Mphasis': 'MPHASIS.NS',
    'KPIT Technologies': 'KPITTECH.NS',
    'Tata Elxsi': 'TATAELXSI.NS',
    'Dixon Technologies': 'DIXON.NS',
    'Oberoi Realty': 'OBEROIRLTY.NS',
    'DLF': 'DLF.NS',
    'Bandhan Bank': 'BANDHANBNK.NS',
    'Federal Bank': 'FEDERALBNK.NS',
    'IndusInd Bank': 'INDUSINDBK.NS',
    'RBL Bank': 'RBLBANK.NS',
    'Nifty 50 ETF (NIFTYBEES)': 'NIFTYBEES.NS',
}

company_names = list(STOCK_SYMBOLS.keys())
selected_company = st.sidebar.selectbox("Select a Stock", options=company_names)
selected_symbol = STOCK_SYMBOLS[selected_company]

# Time period selection
period_options = {
    "1 Day": "1d",
    "5 Days": "5d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "Max": "max"
}
selected_period_label = st.sidebar.selectbox("Select Time Period", options=list(period_options.keys()), index=5)
selected_period = period_options[selected_period_label]

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("This dashboard fetches real-time stock market data using the `yfinance` API, processes it with `pandas`, and visualizes it using `plotly`.")

# Function to fetch data
@st.cache_data(ttl=60) # Cache data for 60 seconds
def load_data(symbol, period):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    data.reset_index(inplace=True)
    return data

# Show loading spinner while data is being fetched
with st.spinner(f'Fetching data for {selected_company} ({selected_symbol})...'):
    try:
        df = load_data(selected_symbol, selected_period)
        
        if df.empty:
            st.warning(f"Failed to fetch data or no data available for {selected_symbol}. Please try another stock or period.")
        else:
            # Layout for metrics
            col1, col2, col3, col4 = st.columns(4)
            
            # Fetch current and previous close
            current_price = df['Close'].iloc[-1]
            previous_price = df['Close'].iloc[-2] if len(df) > 1 else current_price
            price_change = current_price - previous_price
            percent_change = (price_change / previous_price) * 100 if previous_price != 0 else 0
            
            # Additional metrics
            high_price = df['High'].iloc[-1]
            low_price = df['Low'].iloc[-1]
            volume = df['Volume'].iloc[-1]
            
            with col1:
                st.metric(label="Current Price", 
                          value=f"{current_price:.2f}", 
                          delta=f"{price_change:.2f} ({percent_change:.2f}%)")
            with col2:
                st.metric(label="Today's High", value=f"{high_price:.2f}")
            with col3:
                st.metric(label="Today's Low", value=f"{low_price:.2f}")
            with col4:
                st.metric(label="Volume", value=f"{volume:,}")
                
            st.markdown("---")
            
            # Tabs for different visualizations
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Line Chart (Close Price)", "Candlestick Chart", "Historical Data", "AI Price Prediction", "News Sentiment Analysis"])
            
            with tab1:
                st.subheader(f"{selected_company} - Closing Price Trend")
                # Determine line colour: green if trending up, red if down
                line_color = '#10B981' if df['Close'].iloc[-1] >= df['Close'].iloc[0] else '#F87171'
                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(
                    x=df['Date'], y=df['Close'],
                    mode='lines', name='Close Price',
                    line=dict(color=line_color, width=2),
                    fill='tozeroy',
                    fillcolor=f"rgba({'16,185,129' if line_color == '#10B981' else '248,113,113'},0.08)"
                ))
                fig_line.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Price",
                    template="plotly_dark",
                    paper_bgcolor='#1E293B',
                    plot_bgcolor='#1E293B',
                    font=dict(color='#94A3B8'),
                    xaxis=dict(gridcolor='#334155', linecolor='#334155'),
                    yaxis=dict(gridcolor='#334155', linecolor='#334155'),
                    hovermode="x unified",
                    height=500,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig_line, width='stretch')
                
            with tab2:
                st.subheader(f"{selected_company} - Candlestick Chart")
                fig_candle = go.Figure(data=[go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Candlestick',
                    increasing_line_color='#10B981',
                    decreasing_line_color='#F87171',
                    increasing_fillcolor='rgba(16,185,129,0.7)',
                    decreasing_fillcolor='rgba(248,113,113,0.7)'
                )])
                fig_candle.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Price",
                    template="plotly_dark",
                    paper_bgcolor='#1E293B',
                    plot_bgcolor='#1E293B',
                    font=dict(color='#94A3B8'),
                    xaxis=dict(gridcolor='#334155', linecolor='#334155', rangeslider=dict(visible=False)),
                    yaxis=dict(gridcolor='#334155', linecolor='#334155'),
                    height=500,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig_candle, width='stretch')
                
            with tab3:
                st.subheader("Historical Data")
                # Format datetime column for display
                display_df = df.copy()
                if 'Date' in display_df.columns:
                    # Depending on tz-aware datetimes, formatting to string
                    try:
                        display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
                    except Exception:
                        pass
                
                # Show dataframe
                st.dataframe(display_df.sort_values(by='Date', ascending=False), width='stretch')
                
            with tab4:
                st.subheader("🤖 AI Stock Price Prediction (30 Days)")
                st.markdown("This uses the **Prophet** machine learning model developed by Meta to forecast future prices based on historical trends.")
                
                if len(df) < 30:
                    st.warning("Not enough historical data to generate a reliable prediction. Please select a longer time period (e.g., 6 Months, 1 Year).")
                else:
                    with st.spinner("Training ML model & generating forecast..."):
                        # Prepare data for Prophet
                        # Prophet requires columns 'ds' (datetime) and 'y' (value)
                        prophet_df = df[['Date', 'Close']].copy()
                        # Ensure 'Date' is timezone-naive as Prophet expects naive datetimes
                        if prophet_df['Date'].dt.tz is not None:
                            prophet_df['Date'] = prophet_df['Date'].dt.tz_localize(None)
                            
                        prophet_df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
                        
                        # Initialize and fit the model
                        model = Prophet(daily_seasonality=False)
                        model.fit(prophet_df)
                        
                        # Create future dataframe for 30 days
                        future_dates = model.make_future_dataframe(periods=30)
                        
                        # Predict future prices
                        forecast = model.predict(future_dates)
                        
                        # Plotting the forecast
                        fig_pred = go.Figure()
                        
                        # Historical data
                        fig_pred.add_trace(go.Scatter(
                            x=forecast['ds'][:-30], y=forecast['yhat'][:-30],
                            mode='lines', name='Historical Trend',
                            line=dict(color='#10B981', width=2)
                        ))
                        # Predicted data
                        fig_pred.add_trace(go.Scatter(
                            x=forecast['ds'][-30:], y=forecast['yhat'][-30:],
                            mode='lines', name='Predicted Trend',
                            line=dict(color='#F87171', width=2, dash='dash')
                        ))

                        # Confidence bands
                        fig_pred.add_trace(go.Scatter(
                            x=list(forecast['ds'][-30:]) + list(forecast['ds'][-30:])[::-1],
                            y=list(forecast['yhat_upper'][-30:]) + list(forecast['yhat_lower'][-30:])[::-1],
                            fill='toself',
                            fillcolor='rgba(248,113,113,0.12)',
                            line=dict(color='rgba(255,255,255,0)'),
                            hoverinfo="skip",
                            showlegend=False,
                            name='Confidence Interval'
                        ))

                        fig_pred.update_layout(
                            xaxis_title="Date",
                            yaxis_title="Predicted Price",
                            template="plotly_dark",
                            paper_bgcolor='#1E293B',
                            plot_bgcolor='#1E293B',
                            font=dict(color='#94A3B8'),
                            xaxis=dict(gridcolor='#334155', linecolor='#334155'),
                            yaxis=dict(gridcolor='#334155', linecolor='#334155'),
                            hovermode="x unified",
                            height=500,
                            margin=dict(l=0, r=0, t=30, b=0)
                        )
                        st.plotly_chart(fig_pred, width='stretch')
                        
                        # Show prediction data table
                        st.markdown("**Expected Prices for next 7 days:**")
                        recent_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30).head(7)
                        recent_forecast.columns = ['Date', 'Predicted Price', 'Min Expected', 'Max Expected']
                        recent_forecast['Date'] = recent_forecast['Date'].dt.strftime('%Y-%m-%d')
                        st.dataframe(recent_forecast.style.format({
                            'Predicted Price': '{:.2f}', 
                            'Min Expected': '{:.2f}', 
                            'Max Expected': '{:.2f}'
                        }), width='stretch')
                        
            with tab5:
                st.subheader(f"📰 Recent News & Sentiment Analysis for {selected_company}")
                st.markdown("We fetch recent news articles from Yahoo Finance and use NLP to determine if the overall sentiment is **Positive**, **Negative**, or **Neutral**.")
                
                with st.spinner("Fetching news and analyzing sentiment..."):
                    try:
                        # Fetch news for the stock from Yahoo Finance RSS
                        ticker_obj = yf.Ticker(selected_symbol)
                        news = ticker_obj.news
                        
                        if not news:
                            st.info("No recent news found for this stock.")
                        else:
                            sentiments = []
                            for idx, article in enumerate(news[:10]): # Get top 10 news
                                title = article.get('title', '')
                                
                                # Analyze sentiment using TextBlob
                                blob = TextBlob(title)
                                polarity = blob.sentiment.polarity
                                
                                if polarity > 0.1:
                                    sentiment = "Positive 🟢"
                                elif polarity < -0.1:
                                    sentiment = "Negative 🔴"
                                else:
                                    sentiment = "Neutral ⚪"
                                    
                                sentiments.append(polarity)
                                
                                # Display article
                                with st.expander(f"{sentiment} - {title}"):
                                    publisher = article.get('publisher', 'Unknown Publisher')
                                    # Handle different date formats in yahoo finance news
                                    try:
                                        pub_time = datetime.fromtimestamp(article.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M')
                                    except:
                                        pub_time = "Unknown Date"
                                        
                                    st.markdown(f"**Publisher:** {publisher} | **Published:** {pub_time}")
                                    st.markdown(f"🔗 [Read Article]({article.get('link', '#')})")
                            
                            # Calculate overall sentiment
                            if sentiments:
                                avg_polarity = sum(sentiments) / len(sentiments)
                                
                                st.markdown("### Overall Sentiment Summary:")
                                if avg_polarity > 0.1:
                                    st.success("🟢 The overall market sentiment based on recent news is **POSITIVE**.")
                                elif avg_polarity < -0.1:
                                    st.error("🔴 The overall market sentiment based on recent news is **NEGATIVE**.")
                                else:
                                    st.info("⚪ The overall market sentiment based on recent news is **NEUTRAL**.")
                                    
                                st.progress((avg_polarity + 1) / 2) # Maps -1,1 to 0,1
                                st.caption("Sentiment Score Meter (Left = Negative, Right = Positive)")

                    except Exception as news_err:
                        st.warning(f"Could not load news sentiment right now. Error: {news_err}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
