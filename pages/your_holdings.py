import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import generate_micro_chart

def render():
    st.header("Your Holdings (Professional Layout)")

    # --------------------------
    # Stocks Holdings Section
    # --------------------------
    st.subheader("Stocks Holdings")
    df_stocks = pd.DataFrame({
        "Name": ["RELIANCE", "TCS", "INFY"],
        "Price (₹)": [2550, 3150, 1550],
        "Price Change (%)": [1.2, -0.8, 2.0],
        "24h Low (₹)": [2500, 3100, 1500],
        "Quantity": [10, 15, 20]
    })
    df_stocks["Total Value (₹)"] = df_stocks["Price (₹)"] * df_stocks["Quantity"]

    # Create header row for Stocks table
    stocks_header = st.columns([2, 2, 2, 2, 2, 2])
    stocks_header[0].markdown("**Stock Name**")
    stocks_header[1].markdown("**Price (₹)**")
    stocks_header[2].markdown("**Price Change (%)**")
    stocks_header[3].markdown("**24h Low (₹)**")
    stocks_header[4].markdown("**Graph**")
    stocks_header[5].markdown("**Actions**")
    st.markdown("---")

    # Render each row for stocks
    for _, row in df_stocks.iterrows():
        cols = st.columns([2, 2, 2, 2, 2, 2])
        with cols[0]:
            st.write(f"{row['Name']}")
            st.write(f"Qty: {row['Quantity']}")
        with cols[1]:
            st.write(f"₹{row['Price (₹)']}")
        # Color-code the price change
        color = "green" if row["Price Change (%)"] >= 0 else "red"
        with cols[2]:
            st.markdown(f"<span style='color:{color};'>{row['Price Change (%)']}%</span>", unsafe_allow_html=True)
        with cols[3]:
            st.write(f"₹{row['24h Low (₹)']}")
        with cols[4]:
            micro = generate_micro_chart()
            st.plotly_chart(micro, use_container_width=True, config={"displayModeBar": False})
        with cols[5]:
            st.markdown(
                "<button style='background:#3b82f6;color:white;padding:5px 10px;border:none;border-radius:5px;'>Trade</button>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<button style='background:#10b981;color:white;padding:5px 10px;border:none;border-radius:5px;'>Convert</button>",
                unsafe_allow_html=True,
            )
        st.markdown("---")

    # Stocks Total Value Chart with updated labels and colors
    st.write("### Stocks Total Value")
    fig_stocks = go.Figure([go.Bar(
        x=df_stocks["Name"],
        y=df_stocks["Total Value (₹)"],
        marker=dict(
            # Use a list of dark shades for each bar for a more realistic look
            color=['#1f2937', '#374151', '#4b5563'],
            line=dict(color='black', width=1)
        )
    )])
    fig_stocks.update_layout(
        xaxis=dict(
            title="Stock",
            title_font=dict(color='black', size=14),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            title="Total Value (₹)",
            title_font=dict(color='black', size=14),
            tickfont=dict(color='black')
        ),
        margin=dict(l=20, r=20, t=40, b=40),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_stocks, use_container_width=True, config={"displayModeBar": False})

    # ----------------------------
    # Crypto Holdings Section
    # ----------------------------
    st.subheader("Crypto Holdings")
    df_crypto = pd.DataFrame({
        "Name": ["BTC", "ETH"],
        "Price (₹)": [2100000, 245000],
        "Price Change (%)": [2.5, -1.2],
        "24h Low (₹)": [2050000, 240000],
        "Quantity": [0.02, 1.5]
    })
    df_crypto["Total Value (₹)"] = df_crypto["Price (₹)"] * df_crypto["Quantity"]

    # Create header row for Crypto table
    crypto_header = st.columns([2, 2, 2, 2, 2, 2])
    crypto_header[0].markdown("**Crypto Name**")
    crypto_header[1].markdown("**Price (₹)**")
    crypto_header[2].markdown("**Price Change (%)**")
    crypto_header[3].markdown("**24h Low (₹)**")
    crypto_header[4].markdown("**Graph**")
    crypto_header[5].markdown("**Actions**")
    st.markdown("---")

    # Render each row for crypto
    for _, row in df_crypto.iterrows():
        cols = st.columns([2, 2, 2, 2, 2, 2])
        with cols[0]:
            st.write(f"{row['Name']}")
            st.write(f"Qty: {row['Quantity']}")
        with cols[1]:
            st.write(f"₹{row['Price (₹)']}")
        # Color-code the price change
        color = "green" if row["Price Change (%)"] >= 0 else "red"
        with cols[2]:
            st.markdown(f"<span style='color:{color};'>{row['Price Change (%)']}%</span>", unsafe_allow_html=True)
        with cols[3]:
            st.write(f"₹{row['24h Low (₹)']}")
        with cols[4]:
            micro = generate_micro_chart()
            st.plotly_chart(micro, use_container_width=True, config={"displayModeBar": False})
        with cols[5]:
            st.markdown(
                "<button style='background:#3b82f6;color:white;padding:5px 10px;border:none;border-radius:5px;'>Trade</button>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<button style='background:#10b981;color:white;padding:5px 10px;border:none;border-radius:5px;'>Convert</button>",
                unsafe_allow_html=True,
            )
        st.markdown("---")

    # Crypto Total Value Chart with updated labels and colors
    st.write("### Crypto Total Value")
    fig_crypto = go.Figure([go.Bar(
        x=df_crypto["Name"],
        y=df_crypto["Total Value (₹)"],
        marker=dict(
            # Use distinct dark shades for each crypto bar
            color=['#10b981', '#059669'],
            line=dict(color='black', width=1)
        )
    )])
    fig_crypto.update_layout(
        xaxis=dict(
            title="Crypto",
            title_font=dict(color='black', size=14),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            title="Total Value (₹)",
            title_font=dict(color='black', size=14),
            tickfont=dict(color='black')
        ),
        margin=dict(l=20, r=20, t=40, b=40),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_crypto, use_container_width=True, config={"displayModeBar": False})
