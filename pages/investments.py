import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render():
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.header("Investments Dashboard")
    st.write("A detailed analysis of your investment portfolio.")

    # Asset Allocation Pie Chart
    st.subheader("Asset Allocation")
    labels = ['Stocks', 'Bonds', 'Mutual Funds', 'Crypto', 'Paper Trading']
    values = [40, 15, 20, 20, 5]
    fig_allocation = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4, hoverinfo='label+percent')])
    st.plotly_chart(fig_allocation, use_container_width=True, config={"displayModeBar": False})
    
    # Indian Stock Market Holdings
    st.subheader("Indian Stock Market Holdings")
    df_stocks = pd.DataFrame({
        "Stock": ["RELIANCE", "TCS", "HDFC", "INFY"],
        "Investment (₹)": [50000, 40000, 25000, 30000]
    })
    fig_stocks = go.Figure([go.Bar(x=df_stocks["Stock"], y=df_stocks["Investment (₹)"], marker_color='#3b82f6')])
    fig_stocks.update_layout(yaxis_title="Investment (₹)", plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig_stocks, use_container_width=True)
    
    # Crypto Investments
    st.subheader("Crypto Holdings")
    df_crypto = pd.DataFrame({
        "Crypto": ["BTC", "ETH", "SOL", "XRP"],
        "Investment (₹)": [100000, 50000, 20000, 15000]
    })
    fig_crypto = go.Figure([go.Bar(x=df_crypto["Crypto"], y=df_crypto["Investment (₹)"], marker_color='#10b981')])
    fig_crypto.update_layout(yaxis_title="Investment (₹)", plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig_crypto, use_container_width=True)
    
    # Paper Trading Performance
    st.subheader("Paper Trading Performance")
    df_paper_trading = pd.DataFrame({
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "Portfolio Value (₹)": [100000, 102500, 101000, 104000, 106500]
    })
    fig_paper_trading = go.Figure([go.Scatter(x=df_paper_trading["Day"], y=df_paper_trading["Portfolio Value (₹)"], mode='lines+markers', line=dict(color='red'))])
    fig_paper_trading.update_layout(yaxis_title="Portfolio Value (₹)", plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig_paper_trading, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)