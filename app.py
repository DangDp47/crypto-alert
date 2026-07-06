import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Crypto Guardian", layout="wide", page_icon="🚀")

st.title("🚀 Crypto Guardian Dashboard")
st.markdown(f"**Cập nhật:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Sidebar
st.sidebar.header("Cài đặt")
watchlist_input = st.sidebar.text_input("Watchlist (cách nhau bởi dấu phẩy)", "BTC,ETH,SOL,BNB,XRP,DOGE")
watchlist = [x.strip().upper() for x in watchlist_input.split(",")]

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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Top Coin", df.iloc[0]['symbol'].upper(), f"{df.iloc[0]['price_change_percentage_24h']:+.2f}%")
    with col2:
        st.metric("Số coin", len(df))
    with col3:
        st.metric("Thị trường", "Đang theo dõi")

    tab1, tab2, tab3 = st.tabs(["🔥 Top Movers", "⭐ Watchlist", "📊 Chart"])

    with tab1:
        st.subheader("Top Tăng/Giảm 24h")
        gainers = df.nlargest(10, 'price_change_percentage_24h')
        st.dataframe(gainers[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({
            'current_price': '${:,.4f}', 'price_change_percentage_24h': '{:+.2f}%'
        }), use_container_width=True)

    with tab2:
        st.subheader("Watchlist")
        watch_df = df[df['symbol'].str.upper().isin(watchlist)]
        st.dataframe(watch_df[['symbol', 'current_price', 'price_change_percentage_24h', 'market_cap']].style.format({
            'current_price': '${:,.4f}', 'price_change_percentage_24h': '{:+.2f}%'
        }), use_container_width=True)

    with tab3:
        st.subheader("Biểu đồ giá BTC")
        # Simple chart example (can expand)
        st.info("Tính năng chart đầy đủ sẽ thêm ở phiên bản sau")

else:
    st.error("Lỗi lấy dữ liệu. Thử refresh lại.")

st.caption("Crypto Guardian • Dành cho trader 9-5 • Risk trung bình")
