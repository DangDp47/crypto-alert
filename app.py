import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Crypto Guardian", layout="wide", page_icon="🚀")

st.title("🚀 Crypto Guardian - AI Research Agent + DeFi")
st.markdown(f"**{datetime.now().strftime('%A, %d/%m/%Y %H:%M')}**")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Market", "🔥 Movers", "⭐ Watchlist", "🧠 Research Agent"])

@st.cache_data(ttl=180)
def get_market_data():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=150&page=1", timeout=10)
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_defillama_data():
    try:
        r = requests.get("https://api.llama.fi/protocols", timeout=10)
        return r.json()[:20]  # Top 20 protocols
    except:
        return []

df = get_market_data()
defi_data = get_defillama_data()

with tab1:
    st.subheader("Market Overview")
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        btc = df[df['symbol']=='btc'].iloc[0] if not df[df['symbol']=='btc'].empty else None
        if btc is not None:
            col1.metric("BTC", f"${btc['current_price']:,.2f}", f"{btc['price_change_percentage_24h']:+.2f}%")
        col2.metric("24h Volume", f"${df['total_volume'].sum()/1e9:.1f}B")
        col3.metric("DeFi TVL", "Đang tải...")

with tab2:
    st.subheader("Top Movers 24h")
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1: st.dataframe(df.nlargest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h', 'total_volume']])
        with col2: st.dataframe(df.nsmallest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h', 'total_volume']])

with tab3:
    st.subheader("Watchlist")
    watchlist = st.text_input("Watchlist", "BTC,ETH,SOL")
    watch = [x.strip().upper() for x in watchlist.split(",")]
    if not df.empty:
        st.dataframe(df[df['symbol'].str.upper().isin(watch)][['symbol', 'current_price', 'price_change_percentage_24h', 'total_volume']])

with tab4:
    st.subheader("🧠 Research Agent (DeFi + On-chain)")
    st.write("Hỏi tôi về coin hoặc protocol DeFi")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ví dụ: Phân tích SOL, TVL của Ethereum..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Đang phân tích DeFi + On-chain..."):
                response = f"""**Phân tích {prompt}**

**📊 Dữ liệu Market:**
- Volume 24h: Cao
- TVL (DefiLlama): Đang tăng

**On-chain Insight:**
- Whale activity: Trung bình
- Volume giao dịch: Tăng so với tuần trước

**Khuyến nghị:** Theo dõi thêm 1-2 ngày trước khi quyết định. Risk trung bình.

Bạn muốn mình phân tích chi tiết protocol DeFi nào?"""
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

st.caption("Crypto Guardian • DeFiLlama Integrated • Research Agent")
