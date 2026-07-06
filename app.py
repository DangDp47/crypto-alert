import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Crypto Guardian", layout="wide", page_icon="🚀")

st.title("🚀 Crypto Guardian - AI Assistant")
st.markdown(f"**Cập nhật:** {datetime.now().strftime('%d/%m/%Y %H:%M')} | Risk: Trung bình")

# Sidebar
st.sidebar.header("Cài đặt")
watchlist_input = st.sidebar.text_input("Watchlist", "BTC,ETH,SOL,BNB,XRP,DOGE,TON")
watchlist = [x.strip().upper() for x in watchlist_input.split(",")]

alert_price = st.sidebar.number_input("Giá BTC cảnh báo (USD)", value=60000, step=100)

@st.cache_data(ttl=180)
def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=150&page=1"
    try:
        r = requests.get(url, timeout=10)
        return pd.DataFrame(r.json()) if r.status_code == 200 else pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_market_data()

if not df.empty:
    tabs = st.tabs(["🏠 Overview", "🔥 Movers", "⭐ Watchlist", "📈 Chart", "⚠️ Alert"])

    with tabs[0]:
        st.metric("BTC Price", f"${df[df['symbol']=='btc']['current_price'].iloc[0]:,.2f}" if not df[df['symbol']=='btc'].empty else "N/A")

    with tabs[1]:
        st.subheader("Top Movers 24h")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Tăng mạnh")
            st.dataframe(df.nlargest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({"current_price": "${:,.4f}", "price_change_percentage_24h": "{:+.2f}%"}))

        with col2:
            st.write("Giảm mạnh")
            st.dataframe(df.nsmallest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({"current_price": "${:,.4f}", "price_change_percentage_24h": "{:+.2f}%"}))

    with tabs[2]:
        st.subheader("Watchlist")
        watch_df = df[df['symbol'].str.upper().isin(watchlist)]
        st.dataframe(watch_df[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({"current_price": "${:,.4f}", "price_change_percentage_24h": "{:+.2f}%"}))

    with tabs[3]:
        st.subheader("Biểu đồ giá BTC (24h)")
        st.info("Chart đầy đủ sẽ được cải tiến ở lần sau (hiện đang demo)")

    with tabs[4]:
        st.subheader("Cảnh báo giá")
        st.success(f"Đã đặt alert BTC tại ${alert_price:,}")
        st.info("Tính năng alert realtime sẽ được thêm sau (cần background task)")

else:
    st.error("Không lấy được dữ liệu. Kiểm tra kết nối.")

st.caption("Crypto Guardian Agent • Hỗ trợ trader nghiệp dư 9-5")
