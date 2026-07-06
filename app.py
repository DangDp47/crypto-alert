import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Crypto Guardian", layout="wide", page_icon="🚀")

st.title("🚀 Crypto Guardian - AI Research Agent")
st.markdown(f"**{datetime.now().strftime('%A, %d/%m/%Y')}** | Hỗ trợ trader 9-5")

# Sidebar
st.sidebar.header("Research Agent")
st.sidebar.info("Hỏi bất kỳ coin nào bạn muốn phân tích")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Market", "🔥 Movers", "⭐ Watchlist", "🧠 Research Agent"])

@st.cache_data(ttl=180)
def get_market_data():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=150&page=1", timeout=10)
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()

df = get_market_data()

with tab1:
    st.subheader("Market Overview")
    if not df.empty:
        col1, col2 = st.columns(2)
        col1.metric("BTC", "$" + str(df[df['symbol']=='btc']['current_price'].iloc[0] if not df[df['symbol']=='btc'].empty else "N/A"))
        col2.metric("Số coin", len(df))
    else:
        st.error("Không lấy được dữ liệu")

with tab2:
    st.subheader("Top Movers 24h")
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df.nlargest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']])
        with col2:
            st.dataframe(df.nsmallest(10, 'price_change_percentage_24h')[['symbol', 'current_price', 'price_change_percentage_24h']])

with tab3:
    st.subheader("Watchlist")
    watchlist = st.text_input("Coin bạn quan tâm", "BTC,ETH,SOL")
    watch = [x.strip().upper() for x in watchlist.split(",")]
    if not df.empty:
        wdf = df[df['symbol'].str.upper().isin(watch)]
        st.dataframe(wdf[['symbol', 'current_price', 'price_change_percentage_24h']])

with tab4:
    st.subheader("🧠 AI Research Agent")
    st.write("Hỏi tôi bất kỳ điều gì về crypto")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ví dụ: Phân tích SOL, BTC có nên mua không?..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Đang nghiên cứu..."):
                # Simple mock response (có thể kết nối API thật sau)
                response = f"**Phân tích {prompt}**\n\n- Giá hiện tại: Đang cập nhật...\n- Sentiment: Bullish trung bình\n- Rủi ro: Trung bình\n- Khuyến nghị: Theo dõi mức hỗ trợ chính trước khi vào.\n\nBạn muốn phân tích sâu hơn không?"
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

st.caption("Crypto Guardian Research Agent • Đang phát triển")
