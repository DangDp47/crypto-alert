import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Crypto Guardian", layout="wide", page_icon="🚀")

st.title("🚀 Crypto Guardian Dashboard")
st.markdown(f"**Cập nhật lần cuối:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

st.sidebar.header("Cài đặt cá nhân")
watchlist_input = st.sidebar.text_input("Watchlist (cách nhau bởi dấu phẩy)", "BTC,ETH,SOL,BNB,XRP")
watchlist = [x.strip().upper() for x in watchlist_input.split(",")]

@st.cache_data(ttl=180)
def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=150&page=1"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_market_data()

if not df.empty:
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Số coin theo dõi", len(df))
    with col2:
        st.metric("BTC Dominance", "N/A")  # Có thể thêm sau
    with col3:
        st.metric("Thị trường", "Bullish / Bearish")

    # Top Gainers
    st.subheader("🔥 Top Coin Tăng mạnh 24h")
    gainers = df.nlargest(15, 'price_change_percentage_24h')
    st.dataframe(
        gainers[['symbol', 'current_price', 'price_change_percentage_24h', 'market_cap']].style.format({
            'current_price': '${:,.4f}',
            'price_change_percentage_24h': '{:+.2f}%'
        }),
        use_container_width=True,
        height=400
    )

    # Watchlist
    st.subheader("⭐ Watchlist của bạn")
    watch_df = df[df['symbol'].str.upper().isin(watchlist)]
    if not watch_df.empty:
        st.dataframe(watch_df[['symbol', 'current_price', 'price_change_percentage_24h', 'ath_change_percentage']].style.format({
            'current_price': '${:,.4f}',
            'price_change_percentage_24h': '{:+.2f}%'
        }), use_container_width=True)
    else:
        st.info("Chưa có coin nào trong watchlist khớp.")

else:
    st.error("Không thể lấy dữ liệu. Vui lòng thử lại sau.")

st.caption("Powered by CoinGecko • Dành cho trader nghiệp dư • Risk trung bình")
