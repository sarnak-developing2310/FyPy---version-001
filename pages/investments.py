import streamlit as st
import plotly.graph_objects as go

def render():
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.header("Investments")
    st.write("Detailed analysis of your investment portfolio.")
    st.subheader("Asset Allocation")
    labels = ['Stocks', 'Bonds', 'Mutual Funds', 'Others']
    vals = [60, 15, 20, 5]
    fig = go.Figure(data=[go.Pie(labels=labels, values=vals, hole=0.4, hoverinfo='label+percent')])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)