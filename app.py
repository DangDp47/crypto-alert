import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Crypto Guardian", layout="wide", page_icon="🚀")

st.title("🚀 Crypto Guardian - AI Trader")
st.markdown(f"**{datetime.now().strftime('%A, %d/%m/%Y %H:%M')}**")

st.sidebar.header("Cài đặt")
watchlist = st.sidebar.multiselect("Watchlist", ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "TON"], default=["BTC", "ETH", "SOL"])

if st.button("🔄 Refresh Data"):
    st.rerun()

@st.cache_data(ttl=300)
def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=150&page=1"
    try:
        r = requests.get(url, timeout=10)
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()

df = get_market_data()

if not df.empty:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Overview", "🔥 Top Movers", "⭐ Watchlist + S/R", "📰 News & Sentiment"])

    with tab1:
        st.subheader("Top 150 Coin Market")
        st.dataframe(df[['symbol', 'current_price', 'price_change_percentage_24h', 'market_cap_rank']].style.format({
            'current_price': '${:,.4f}',
            'price_change_percentage_24h': '{:+.2f}%'
        }), height=600)

    with tab2:
        st.subheader("Top Movers 24h")
        col1, col2 = st.columns(2)
        with col1:
            st.write("🟢 Tăng mạnh")
            st.dataframe(df.nlargest(15, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']])
        with col2:
            st.write("🔴 Giảm mạnh")
            st.dataframe(df.nsmallest(15, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']])

    with tab3:
        st.subheader("Watchlist + Mức giá quan trọng")
        watch_df = df[df['symbol'].str.upper().isin(watchlist)]
        st.dataframe(watch_df[['symbol', 'current_price', 'price_change_percentage_24h', 'ath', 'atl']])

        st.info("Mức hỗ trợ/kháng cự sẽ được phân tích chi tiết hơn ở phiên bản sau")

    with tab4:
        st.subheader("📰 Tin tức & Sentiment (Demo)")
        st.info("Tính năng lấy tin tức + sentiment X đang được tích hợp. Hiện hiển thị placeholder.")
        st.warning("Không có tin tức lớn trong 24h qua.")
        st.success("Sentiment tổng thể: Neutral - Bullish nhẹ")

else:
    st.error("Không lấy được dữ liệu. Kiểm tra kết nối.")

st.caption("Crypto Guardian Agent • Dành cho trader 9-5 • Risk Trung bình")
