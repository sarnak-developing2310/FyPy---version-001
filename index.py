import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
from streamlit_option_menu import option_menu
from styles import inject_css
import pages.dashboard as dashboard
import pages.ai_advisor as ai_advisor
import pages.investments as investments
# import pages.reports as reports
import pages.stocks as stocks
import pages.crypto as crypto
import pages.paper_trading as paper_trading
import pages.your_holdings as your_holdings
import pages.profile as profile
import pages.settings as settings
import pages.login as login
import pages.signup as signup

st.set_page_config(page_title="FyPy", page_icon="💎", layout="wide")

# Increase title font size using Markdown & CSS
st.markdown(
    """
    <style>
    .title {
        font-size: 42px !important;
        font-weight: bold;
        text-align: center;
        color: #333;
    }
    </style>
    <h1 class='title'>💎 Finance Hub</h1>
    """,
    unsafe_allow_html=True
)

# ✅ Inject CSS only if styles.py exists
try:
    from styles import inject_css
    inject_css()
except ImportError:
    st.warning("Styles module not found! Skipping custom CSS.")

pages_map = {
    "Dashboard": dashboard.render,
    "Login": login.render,
    "Signup": signup.render,
    "Equity Analysis Bot": ai_advisor.show_page,
    "Investments": investments.render,
    # "Reports": reports.render,
    "Stocks": stocks.show_page,
    "Crypto": crypto.show_page,
    "Paper Trading": paper_trading.render,
    "Your Holdings": your_holdings.render,
    "Profile": profile.render,
    "Settings": settings.render
}

selected_page = st.sidebar.radio("Navigation", list(pages_map.keys()))
pages_map[selected_page]()
