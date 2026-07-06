import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Crypto Guardian", layout="wide", page_icon="🚀")

st.title("🚀 Crypto Guardian Dashboard")
st.markdown(f"**Cập nhật:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.sidebar.header("Watchlist")
watchlist_input = st.sidebar.text_input("Coin bạn quan tâm (cách bởi dấu phẩy)", "BTC,ETH,SOL,BNB,XRP,DOGE,TON")
watchlist = [x.strip().upper() for x in watchlist_input.split(",")]

@st.cache_data(ttl=300)
def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=150&page=1"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_market_data()

if not df.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔥 Top Tăng 24h")
        st.dataframe(df.nlargest(8, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({
            'current_price': '${:,.4f}',
            'price_change_percentage_24h': '{:+.2f}%'
        }), use_container_width=True)
    
    with col2:
        st.subheader("📉 Top Giảm 24h")
        st.dataframe(df.nsmallest(8, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']].style.format({
            'current_price': '${:,.4f}',
            'price_change_percentage_24h': '{:+.2f}%'
        }), use_container_width=True)

    st.subheader("⭐ Watchlist")
    watch_df = df[df['symbol'].str.upper().isin(watchlist)]
    if not watch_df.empty:
        st.dataframe(watch_df[['symbol', 'current_price', 'price_change_percentage_24h', 'market_cap_rank']].style.format({
            'current_price': '${:,.4f}',
            'price_change_percentage_24h': '{:+.2f}%'
        }), use_container_width=True)
    else:
        st.warning("Không tìm thấy coin trong watchlist.")

else:
    st.error("Không lấy được dữ liệu từ CoinGecko. Hãy thử refresh trang.")

st.caption("Crypto Guardian Agent • Hỗ trợ trader 9-5 • Risk trung bình")
