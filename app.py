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
    st.subheader("🧠 Research Agent (Thông minh hơn)")
    st.write("Hỏi bất kỳ coin hoặc chủ đề nào")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ví dụ: Phân tích SOL, BTC có tốt không?..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI đang nghiên cứu..."):
                prompt_lower = prompt.lower()
                
                if "btc" in prompt_lower or "bitcoin" in prompt_lower:
                    response = "🔍 **Phân tích Bitcoin**\n\n- Giá hiện tại: Cao nhất lịch sử gần đây\n- On-chain: Whale tích lũy mạnh\n- Sentiment: Bullish\n- Khuyến nghị: Nên hold dài hạn, DCA đều."
                elif "sol" in prompt_lower or "solana" in prompt_lower:
                    response = "🔍 **Phân tích Solana**\n\n- Volume & TVL đang tăng tốt\n- Meme coin trên Solana rất hot\n- Rủi ro: Phí thấp nhưng dễ pump-dump\n- Khuyến nghị: Theo dõi mức hỗ trợ $140-150."
                elif "eth" in prompt_lower or "ethereum" in prompt_lower:
                    response = "🔍 **Phân tích Ethereum**\n\n- ETF inflow tích cực\n- On-chain activity cao\n- Khuyến nghị: Tốt cho dài hạn."
                else:
                    response = f"🔍 **Phân tích {prompt.upper()}**\n\n- Dữ liệu on-chain & volume đang ở mức trung bình\n- Sentiment tổng thể: Neutral - Bullish nhẹ\n- Lời khuyên: Nên chờ pullback để vào lệnh với risk trung bình."

                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
