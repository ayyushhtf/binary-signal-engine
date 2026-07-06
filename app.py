import streamlit as st
import pandas as pd
import ccxt
import ta
import time

# Mobile responsive UI and Page Config
st.set_page_config(page_title="World No.1 Binary Engine", page_icon="📈", layout="centered")

# Dark Theme styling custom CSS
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; color: white; }
    .metric-box { padding: 15px; border-radius: 10px; background-color: #1f2937; text-align: center; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI-Based Signal Engine")
st.subheader("Live Binary Options Analysis Dashboard")
st.write("---")

# Settings on Screen
symbol = st.selectbox("Select Asset / Pair", ["BTC/USDT", "ETH/USDT", "LTC/USDT"])
timeframe = st.selectbox("Select Timeframe", ["1m", "5m", "15m"])

# Initialize Exchange
exchange = ccxt.binance({'rateLimit': 1200, 'enableRateLimit': True})

def fetch_data(symbol, timeframe):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df
    except:
        return None

# Placeholder for live updates
placeholder = st.empty()

# Run continuous loop
while True:
    df = fetch_data(symbol, timeframe)
    
    if df is not None:
        with placeholder.container():
            # Indicators Logic
            current_price = df['close'].iloc[-1]
            ema9 = ta.trend.ema_indicator(df['close'], window=9).iloc[-1]
            ema21 = ta.trend.ema_indicator(df['close'], window=21).iloc[-1]
            rsi = ta.momentum.rsi(df['close'], window=14).iloc[-1]
            macd_line = ta.trend.macd(df['close']).iloc[-1]
            macd_signal = ta.trend.macd_signal(df['close']).iloc[-1]
            
            # Vote Engine
            up_votes = 0
            total_votes = 4
            
            if current_price > ema9: up_votes += 1
            if ema9 > ema21: up_votes += 1
            if rsi < 40: up_votes += 1  # Oversold support
            if macd_line > macd_signal: up_votes += 1
            
            up_score = int((up_votes / total_votes) * 100)
            down_score = 100 - up_score
            
            # --- DISPLAY FOR MOBILE ---
            st.metric(label=f"Live Price ({symbol})", value=f"${current_price}")
            
            col1, col2 = st.columns(2)
            col1.markdown(f"<div class='metric-box'><h3 style='color:#22c55e;'>🟢 UP Score</h3><h2>{up_score}%</h2></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='metric-box'><h3 style='color:#ef4444;'>🔴 DOWN Score</h3><h2>{down_score}%</h2></div>", unsafe_allow_html=True)
            
            # Final Signal Decision
            if up_score >= 75:
                st.success("🔥 SIGNAL: STRONG UP (BUY) 🟢")
            elif down_score >= 75:
                st.error("🔥 SIGNAL: STRONG DOWN (SELL) 🔴")
            else:
                st.warning("⏳ SIGNAL: NEUTRAL (Wait for strong trend) ⚪")
                
            st.caption("Auto-refreshing every 10 seconds...")
            
    time.sleep(10)
