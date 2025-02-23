import streamlit as st

def inject_css():
    css = """
    <style>
    :root {
      --font-family: 'Inter', sans-serif;
      --primary-color: #00b383;
      --bg-light: #f2f4f8;
      --bg-dark: #1e1e1e;
      --text-light: #000000;
      --text-dark: #ffffff;
      --card-bg-light: #ffffff;
      --card-bg-dark: #2e2e2e;
      --transition-speed: 0.3s;
    }
    
    html, body, [class*="css"] {
      font-family: var(--font-family);
      transition: background-color var(--transition-speed), color var(--transition-speed);
    }
    
    body {
      background-color: var(--bg-light);
      color: var(--text-light);
      margin: 0;
      padding: 0;
    }
    
    /* Report view container */
    .reportview-container {
      background: var(--bg-light);
    }
    
    /* Title styling */
    .shiny-title {
      font-size: 48px;
      font-weight: 700;
      text-align: center;
      background: linear-gradient(90deg, var(--primary-color), #00a173);
      background-size: 200% auto;
      color: transparent;
      -webkit-background-clip: text;
      animation: shine 3s linear infinite;
      margin-bottom: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    /* Sticky Auth (top-right) */
    .sticky-auth {
      position: fixed;
      top: 60px;
      right: 20px;
      z-index: 1100;
      display: flex;
      gap: 10px;
    }
    .sticky-auth a {
      background: var(--card-bg-light);
      color: var(--text-light);
      padding: 8px 12px;
      border-radius: 5px;
      text-decoration: none;
      font-weight: 500;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      transition: transform 0.3s ease;
    }
    .sticky-auth a:hover { transform: scale(1.1); }
    
    /* Sidebar Override */
    .css-1d391kg {
      background-color: #ffffff !important;
      border-right: 1px solid #ccc;
    }
    
    /* Metric Cards using flexbox */
    .flex-container {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      justify-content: space-around;
    }
    .metric-card {
      background: linear-gradient(135deg, var(--card-bg-light), var(--card-bg-light));
      border-radius: 12px;
      padding: 20px;
      min-width: 220px;
      text-align: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      transition: transform 0.3s ease;
    }
    .metric-card:hover { transform: scale(1.05); }
    
    /* Page content card */
    .card {
      background: var(--card-bg-light);
      border-radius: 8px;
      padding: 15px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      margin-bottom: 20px;
    }
    
    /* Table styling */
    table.dataframe {
      font-size: 18px;
      width: 100%;
    }
    table.dataframe tbody tr:hover {
      background-color: #eef3f7;
      transform: scale(1.02);
      transition: transform 0.3s ease;
    }
    
    /* Fade-in animation */
    .fade-in { animation: fadeIn 0.8s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    
    /* Dark Mode Overrides */
    body.dark-mode {
      background-color: var(--bg-dark);
      color: var(--text-dark);
    }
    body.dark-mode .card {
      background: var(--card-bg-dark);
    }
    body.dark-mode .metric-card {
      background: var(--card-bg-dark);
      color: var(--text-dark);
    }
    body.dark-mode .css-1d391kg {
      background-color: #2a2a2a !important;
      border-right: 1px solid #444;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
