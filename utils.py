import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

def generate_time_series(start_date, end_date, base, trend_factor, noise=0.05):
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    values = [base + (i * trend_factor) + (i**2 * 0.1) + np.random.randn()*noise*base for i in range(len(dates))]
    return pd.DataFrame({'Date': dates, 'Value': values})

def generate_micro_chart():
    now = datetime.now()
    times = pd.date_range(start=now - timedelta(hours=24), end=now, freq='H')
    base = np.random.uniform(100, 1000)
    values = np.cumsum(np.random.randn(len(times))) + base
    df = pd.DataFrame({'Time': times, 'Value': values})
    up = values[-1] >= values[0]
    color = "#00c853" if up else "#d50000"
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Time'],
        y=df['Value'],
        mode='lines',
        line=dict(color=color, width=2),
        hoverinfo='none'
    ))
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
        height=40, width=120,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def trend_color(up=True):
    return "rgba(144,238,144,0.5)" if up else "rgba(255,182,193,0.5)"
    