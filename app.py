import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Thêm đường dẫn để import Jesse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Jesse + Streamlit", layout="wide")
st.title("🚀 Jesse Trading Bot - Streamlit Deep Integration")

# Sidebar config
st.sidebar.header("Cấu hình")
symbol = st.sidebar.text_input("Symbol", "BTC-USDT")
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"])
start_date = st.sidebar.date_input("Ngày bắt đầu", datetime(2024, 1, 1))
end_date = st.sidebar.date_input("Ngày kết thúc", datetime.now())

strategy_name = st.sidebar.text_input("Tên Strategy", "MyStrategy")

if st.sidebar.button("Chạy Backtest"):
    with st.spinner("Đang chạy backtest..."):
        try:
            from jesse import research
            from jesse.strategies import Strategy
            
            # Import hoặc tạo strategy động
            config = {
                'starting_balance': 10000,
                'fee': 0.001,
                'type': 'futures',
                'exchange': 'Binance',
                'symbol': symbol,
                'timeframe': timeframe,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
            }
            
            # Chạy backtest
            result = research.backtest(
                strategy_class=YourStrategy,  # Thay bằng class strategy của bạn
                config=config
            )
            
            st.success("Backtest hoàn thành!")
            
            # Hiển thị kết quả
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tổng lợi nhuận", f"{result['total_profit']:.2f}%")
            with col2:
                st.metric("Số trade", result['total_trades'])
            with col3:
                st.metric("Win Rate", f"{result['win_rate']:.1f}%")
            
            # Chart
            if 'equity_curve' in result:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=result['dates'], y=result['equity_curve'], name='Equity'))
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Lỗi: {str(e)}")
            st.info("Kiểm tra console để xem chi tiết lỗi")

# Hiển thị danh sách strategies hiện có
st.subheader("Các Strategy hiện có")
strategies = os.listdir("strategies") if os.path.exists("strategies") else []
st.write(strategies)
