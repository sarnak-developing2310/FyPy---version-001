import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils import generate_time_series

def render():
    st.header("Financial Dashboard")

    # ✅ Creating columns for metrics
    col1, col2, col3, col4 = st.columns(4)

    # ✅ Styling Function for Metrics
    def metric_card(container, title, value, change, color):
        container.markdown(
            f"""
            <div style="
                background-color: {color}; 
                padding: 15px; 
                border-radius: 10px; 
                text-align: center; 
                color: white;
                font-size: 18px;">
                <strong>{title}</strong>
                <br>
                <span style="font-size: 24px; font-weight: bold;">{value}</span>
                <br>
                <span style="font-size: 14px;">{change}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ✅ Adding Metrics to Columns
    metric_card(col1, "Portfolio Value", "₹32,50,000", "+1.45%", "#1E90FF")  # Blue
    metric_card(col2, "Stock Performance", "+8.7%", "+0.85%", "#32CD32")  # Green
    metric_card(col3, "Crypto Holdings", "₹5,20,000", "-0.75%", "#FF4500")  # Orange
    metric_card(col4, "Paper Trading P/L", "+₹75,000", "+2.15%", "#8A2BE2")  # Purple

    # ✅ Portfolio Performance Chart
    st.subheader("Portfolio Performance")
    df = generate_time_series("2024-01-01", "2024-03-14", 3200000, 5000)
    idx = st.slider("Select Day to Highlight", 0, len(df)-1, 10)
    sel_date = df.iloc[idx]['Date']
    sel_val = df.iloc[idx]['Value']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Value'],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#3b82f6', width=2),
        hovertemplate='Date: %{x|%b %d, %Y}<br>Value: ₹%{y:,.0f}<extra></extra>'
    ))
    fig.add_vline(x=sel_date, line_width=2, line_dash="dot", line_color="orange")
    fig.add_annotation(
        x=sel_date, y=sel_val,
        text=f"₹{sel_val:,.0f}",
        showarrow=True, arrowhead=1, ax=40, ay=-40
    )
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20, l=20, r=20, b=20),
        xaxis=dict(showgrid=True, gridcolor='#e5e5e5'),
        yaxis=dict(showgrid=True, gridcolor='#e5e5e5', tickprefix='₹')
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ✅ Recent Activity - Stylish Table
    st.subheader("Recent Activity")

    # Sample data
    activities = [
        {"Action": "Bought INFY", "Details": "50 shares at ₹1,600", "Time": "2h ago"},
        {"Action": "Sold TCS", "Details": "30 shares at ₹3,200", "Time": "5h ago"},
        {"Action": "Bought BTC", "Details": "0.01 BTC at ₹20,00,000", "Time": "1d ago"}
    ]

    # Convert list to DataFrame
    df_activities = pd.DataFrame(activities)

    # ✅ Custom CSS for Improved Table Styling
    st.markdown("""
        <style>
            .activity-table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                font-size: 16px;
                text-align: left;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            }
            .activity-table th {
                background-color: #0047AB;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: bold;
            }
            .activity-table td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
                background-color: #f9f9f9;
                color: #333;
            }
            .activity-table tr:nth-child(even) td {
                background-color: #E6F0FF;
            }
            .activity-table tr:hover td {
                background-color: #C9DEFF;
                color: black;
            }
        </style>
    """, unsafe_allow_html=True)

    # ✅ Convert DataFrame to HTML with Custom Styling
    table_html = df_activities.to_html(index=False, classes="activity-table", escape=False)

    # ✅ Render the Styled Table in Streamlit
    st.markdown(table_html, unsafe_allow_html=True)