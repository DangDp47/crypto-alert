import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Crypto Guardian", layout="wide", page_icon="🚀")

st.title("🚀 Crypto Guardian - AI Trader Assistant")

st.sidebar.header("Cài đặt")
watchlist_input = st.sidebar.text_input("Watchlist", "BTC,ETH,SOL")
watchlist = [x.strip().upper() for x in watchlist_input.split(",")]

@st.cache_data(ttl=60)
def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=150&page=1"
    try:
        r = requests.get(url, timeout=10)
        return pd.DataFrame(r.json()) if r.status_code == 200 else pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_market_data()

if not df.empty:
    tabs = st.tabs(["Overview", "Movers", "Watchlist", "📈 Chart", "⚠️ Alert"])

    with tabs[0]:
        btc = df[df['symbol'] == 'btc'].iloc[0] if not df[df['symbol'] == 'btc'].empty else None
        if btc is not None:
            st.metric("BTC/USDT", f"${btc['current_price']:,.2f}", f"{btc['price_change_percentage_24h']:+.2f}%")

    with tabs[1]:
        st.subheader("Top Movers 24h")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df.nlargest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({"current_price": "${:,.4f}", "price_change_percentage_24h": "{:+.2f}%"}))

        with col2:
            st.dataframe(df.nsmallest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({"current_price": "${:,.4f}", "price_change_percentage_24h": "{:+.2f}%"}))

    with tabs[2]:
        st.subheader("Your Watchlist")
        watch_df = df[df['symbol'].str.upper().isin(watchlist)]
        st.dataframe(watch_df[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({"current_price": "${:,.4f}", "price_change_percentage_24h": "{:+.2f}%"}))

    with tabs[3]:
        st.subheader("📈 Biểu đồ giá (BTC)")
        # Lấy dữ liệu lịch sử cho BTC
        hist_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7"
        try:
            hist = requests.get(hist_url).json()
            prices = hist['prices']
            df_chart = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df_chart['date'] = pd.to_datetime(df_chart['timestamp'], unit='ms')
            fig = px.line(df_chart, x='date', y='price', title="BTC 7 Days Price")
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("Đang tải chart...")

    with tabs[4]:
        st.subheader("Cảnh báo giá")
        alert_price = st.number_input("Giá BTC muốn nhận cảnh báo", value=65000, step=500)
        st.success(f"Đã đặt alert: Khi BTC chạm ~${alert_price:,} sẽ thông báo (tính năng đang phát triển)")

else:
    st.error("Không lấy được dữ liệu từ CoinGecko.")

st.caption("Crypto Guardian • Hỗ trợ trader part-time")
