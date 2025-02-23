import streamlit as st
from utils import generate_time_series, generate_micro_chart

def render():
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.header("Paper Trading")
    
    # Execute Trade Section
    st.subheader("Execute Trade")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        action = st.selectbox("Trade Action", ["Buy", "Sell"])
    with c2:
        asset = st.selectbox("Asset", ["INFY", "TCS", "RELIANCE", "BTC", "ETH"])
    with c3:
        qty = st.number_input("Quantity", min_value=1, value=10)
    with c4:
        pr = st.number_input("Price per Unit (₹)", min_value=0.0, value=100.0)
    if st.button("Execute Trade"):
        st.success(f"Simulated {action} order for {qty} units of {asset} at ₹{pr} each.")
    
    # Holdings Table
    st.subheader("Your Paper Trading Holdings")
    holdings = [
        {"Name": "INFY", "Price": 1650, "Change": 3.0, "Low": 1600, "Quantity": 100},
        {"Name": "TCS", "Price": 3150, "Change": -1.2, "Low": 3100, "Quantity": 50},
        {"Name": "BTC", "Price": 2100000, "Change": 2.1, "Low": 2050000, "Quantity": 0.05}
    ]
    st.write("**Name | Price | Price Change | 24h Low | Graph | Actions**")
    st.write("---")
    for row in holdings:
        c1, c2, c3, c4, c5, c6 = st.columns([2,2,2,2,2,2])
        with c1:
            st.write(f"**{row['Name']}**")
            st.write(f"Qty: {row['Quantity']}")
        with c2:
            st.write(f"₹{row['Price']}")
        with c3:
            color = "green" if row["Change"] >= 0 else "red"
            st.markdown(f"<span style='color:{color};'>{row['Change']}%</span>", unsafe_allow_html=True)
        with c4:
            st.write(f"₹{row['Low']}")
        with c5:
            micro = generate_micro_chart()
            st.plotly_chart(micro, use_container_width=True, config={"displayModeBar": False})
        with c6:
            st.write("**Trade**")
            st.write("**Convert**")
        st.markdown("---")
    
    st.subheader("Transaction History")
    transactions = [
        {"Date": "2024-03-10", "Asset": "INFY", "Action": "Buy", "Quantity": 50, "Price": 1620},
        {"Date": "2024-03-11", "Asset": "BTC", "Action": "Buy", "Quantity": 0.02, "Price": 2050000},
        {"Date": "2024-03-12", "Asset": "TCS", "Action": "Sell", "Quantity": 20, "Price": 3180}
    ]
    st.table(transactions)
    st.markdown("</div>", unsafe_allow_html=True)