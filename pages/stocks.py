import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils import generate_time_series, trend_color, generate_micro_chart

def render():
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.header("Stocks Forecasting & Analysis")
    st.write("View live Indian stock market trends and forecasts.")
    
    df_stocks = st.dataframe({
        "Name": ["RELIANCE", "TCS", "INFY", "HDFC", "GTLINF!"],
        "Price (₹)": [2500, 3200, 1500, 2800, 80],
        "Price Change (%)": [0.75, -0.50, 1.20, -0.30, -3.50]
    })  # Replace st.dataframe with a DataFrame display if desired.
    
    st.subheader("Market Overview")
    st.write("**Name | Price | Price Change | 24h Low | Graph | Actions**")
    st.write("---")
    
    # Sample data – here we use a loop to simulate rows
    stocks = [
        {"Name": "RELIANCE", "Price": 2500, "Change": 0.75, "Low": 2450},
        {"Name": "TCS", "Price": 3200, "Change": -0.50, "Low": 3100},
        {"Name": "INFY", "Price": 1500, "Change": 1.20, "Low": 1450},
        {"Name": "HDFC", "Price": 2800, "Change": -0.30, "Low": 2750},
        {"Name": "GTLINF!", "Price": 80, "Change": -3.50, "Low": 75}
    ]
    for row in stocks:
        c1, c2, c3, c4, c5, c6 = st.columns([2,2,2,2,2,2])
        with c1:
            st.write(f"**{row['Name']}**")
        with c2:
            st.write(f"₹{row['Price']}")
        with c3:
            change_color = "green" if row["Change"] >= 0 else "red"
            st.markdown(f"<span style='color:{change_color};'>{row['Change']}%</span>", unsafe_allow_html=True)
        with c4:
            st.write(f"₹{row['Low']}")
        with c5:
            micro = generate_micro_chart()
            st.plotly_chart(micro, use_container_width=True, config={"displayModeBar": False})
        with c6:
            st.write("**Trade**")
            st.write("**Convert**")
        st.markdown("---")
    
    st.subheader("Detailed Stock Forecast")
    stock_choice = st.selectbox("Select Stock", [s["Name"] for s in stocks])
    df_pred = generate_time_series("2024-03-15", "2024-03-30", 1500 if stock_choice != "GTLINF!" else 80, 20)
    fig = go.Figure()
    up = df_pred['Value'].iloc[-1] >= df_pred['Value'].iloc[0]
    fig.add_trace(go.Scatter(
        x=df_pred['Date'], y=df_pred['Value'],
        mode='lines+markers',
        name=f'{stock_choice} Prediction',
        line=dict(color=trend_color(up), width=3),
        marker=dict(size=6),
        hovertemplate='Date: %{x|%b %d, %Y}<br>Predicted Price: ₹%{y:,.0f}<extra></extra>'
    ))
    if stock_choice == "GTLINF!":
        st.warning("GTL Infrastructures marked as **RISKY**!")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)