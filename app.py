import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Crypto Guardian", layout="wide", page_icon="🚀")

st.title("🚀 Crypto Guardian - AI Trader Assistant")
st.markdown(f"**Cập nhật:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.sidebar.header("Cài đặt")
watchlist_input = st.sidebar.text_input("Watchlist", "BTC,ETH,SOL,BNB")
watchlist = [x.strip().upper() for x in watchlist_input.split(",")]

if st.button("🔄 Refresh All Data"):
    st.rerun()

@st.cache_data(ttl=180)
def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=150&page=1"
    try:
        r = requests.get(url, timeout=10)
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()

df = get_market_data()

if not df.empty:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🔥 Movers", "⭐ Watchlist", "📈 Chart", "🧠 Sentiment & News"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        btc = df[df['symbol']=='btc'].iloc[0] if not df[df['symbol']=='btc'].empty else None
        if btc is not None:
            col1.metric("BTC", f"${btc['current_price']:,.2f}", f"{btc['price_change_percentage_24h']:+.2f}%")
        col2.metric("Top 150 Coins", len(df))
        col3.metric("Market Trend", "Neutral-Bullish")

    with tab2:
        st.subheader("Top Movers 24h")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🟢 Gainers")
            st.dataframe(df.nlargest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({"current_price": "${:,.4f}", "price_change_percentage_24h": "{:+.2f}%"}))

        with col2:
            st.subheader("🔴 Losers")
            st.dataframe(df.nsmallest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({"current_price": "${:,.4f}", "price_change_percentage_24h": "{:+.2f}%"}))

    with tab3:
        st.subheader("⭐ Watchlist")
        watch_df = df[df['symbol'].str.upper().isin(watchlist)]
        st.dataframe(watch_df[['symbol', 'current_price', 'price_change_percentage_24h', 'market_cap_rank']].style.format({"current_price": "${:,.4f}", "price_change_percentage_24h": "{:+.2f}%"}))

    with tab4:
        st.subheader("📈 Biểu đồ BTC 7 ngày")
        try:
            hist = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7").json()['prices']
            df_chart = pd.DataFrame(hist, columns=['time', 'price'])
            df_chart['date'] = pd.to_datetime(df_chart['time'], unit='ms')
            fig = px.line(df_chart, x='date', y='price', title="BTC Price - 7 Days")
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("Đang tải chart BTC...")

    with tab5:
        st.subheader("🧠 Sentiment Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            sentiment_score = 65  # Demo
            fig = px.pie(values=[sentiment_score, 100-sentiment_score], names=['Bullish', 'Bearish'], title="Market Sentiment")
            st.plotly_chart(fig)
        
        with col2:
            st.metric("Sentiment Score", f"{sentiment_score}/100", "Bullish")
        
        st.subheader("Tin tức nổi bật 24h")
        st.info("• Không có tin FUD lớn")
        st.success("• ETF Bitcoin inflow tích cực")
        st.warning("• Whale di chuyển 5,000 BTC")

else:
    st.error("Lỗi kết nối dữ liệu.")

st.caption("Crypto Guardian Agent • Hỗ trợ trader nghiệp dư")
