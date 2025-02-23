import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import generate_micro_chart

def render():
    st.markdown("<div class='fade-in card' style='min-height:80vh;'>", unsafe_allow_html=True)
    st.header("Your Holdings (Professional Layout)")
    
    st.subheader("Stocks Holdings")
    df_stocks = pd.DataFrame({
        "Name": ["RELIANCE", "TCS", "INFY"],
        "Price (₹)": [2550, 3150, 1550],
        "Price Change (%)": [1.2, -0.8, 2.0],
        "24h Low (₹)": [2500, 3100, 1500],
        "Quantity": [10, 15, 20]
    })
    df_stocks["Total Value (₹)"] = df_stocks["Price (₹)"] * df_stocks["Quantity"]
    
    st.write("**Name | Price | Price Change | 24h Low | Graph | Actions**")
    st.write("---")
    for _, row in df_stocks.iterrows():
        c1, c2, c3, c4, c5, c6 = st.columns([2,2,2,2,2,2])
        with c1:
            st.write(f"**{row['Name']}**")
            st.write(f"Qty: {row['Quantity']}")
        with c2:
            st.write(f"₹{row['Price (₹)']}")
        color = "green" if row["Price Change (%)"] >= 0 else "red"
        with c3:
            st.markdown(f"<span style='color:{color};'>{row['Price Change (%)']}%</span>", unsafe_allow_html=True)
        with c4:
            st.write(f"₹{row['24h Low (₹)']}")
        with c5:
            micro = generate_micro_chart()
            st.plotly_chart(micro, use_container_width=True, config={"displayModeBar": False})
        with c6:
            st.write("**Trade**")
            st.write("**Convert**")
        st.markdown("---")
    
    st.write("### Stocks Total Value")
    fig_stocks = go.Figure([go.Bar(
        x=df_stocks["Name"],
        y=df_stocks["Total Value (₹)"],
        marker_color="#3b82f6"
    )])
    fig_stocks.update_layout(
        margin=dict(l=20, r=20, t=40, b=40),
        xaxis_title="Stock",
        yaxis_title="Total Value (₹)",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_stocks, use_container_width=True, config={"displayModeBar": False})
    
    st.subheader("Crypto Holdings")
    df_crypto = pd.DataFrame({
        "Name": ["BTC", "ETH"],
        "Price (₹)": [2100000, 245000],
        "Price Change (%)": [2.5, -1.2],
        "24h Low (₹)": [2050000, 240000],
        "Quantity": [0.02, 1.5]
    })
    df_crypto["Total Value (₹)"] = df_crypto["Price (₹)"] * df_crypto["Quantity"]
    
    st.write("**Name | Price | Price Change | 24h Low | Graph | Actions**")
    st.write("---")
    for _, row in df_crypto.iterrows():
        c1, c2, c3, c4, c5, c6 = st.columns([2,2,2,2,2,2])
        with c1:
            st.write(f"**{row['Name']}**")
            st.write(f"Qty: {row['Quantity']}")
        with c2:
            st.write(f"₹{row['Price (₹)']}")
        color = "green" if row["Price Change (%)"] >= 0 else "red"
        with c3:
            st.markdown(f"<span style='color:{color};'>{row['Price Change (%)']}%</span>", unsafe_allow_html=True)
        with c4:
            st.write(f"₹{row['24h Low (₹)']}")
        with c5:
            micro = generate_micro_chart()
            st.plotly_chart(micro, use_container_width=True, config={"displayModeBar": False})
        with c6:
            st.write("**Trade**")
            st.write("**Convert**")
        st.markdown("---")
    
    st.write("### Crypto Total Value")
    fig_crypto = go.Figure([go.Bar(
        x=df_crypto["Name"],
        y=df_crypto["Total Value (₹)"],
        marker_color="#10b981"
    )])
    fig_crypto.update_layout(
        margin=dict(l=20, r=20, t=40, b=40),
        xaxis_title="Coin",
        yaxis_title="Total Value (₹)",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_crypto, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown("</div>", unsafe_allow_html=True)