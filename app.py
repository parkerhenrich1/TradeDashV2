import streamlit as st

from modules.dashboard import show_dashboard
from modules.rankings import show_rankings
from modules.research import show_research
from modules.journal import show_journal
from modules.risk_calculator import show_risk_calculator

st.set_page_config(
    page_title="TradeDash",
    page_icon="📈",
    layout="wide"
)

st.title("📈 TradeDash Terminal")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Rankings",
        "Research",
        "Journal",
        "Risk Calculator"
    ]
)

if page == "Dashboard":
    show_dashboard()

elif page == "Rankings":
    show_rankings()

elif page == "Research":
    show_research()

elif page == "Journal":
    show_journal()

elif page == "Risk Calculator":
    show_risk_calculator()

import subprocess

if st.sidebar.button(
    "🔄 Refresh Market"
):
    with st.spinner(
        "Updating Scanner..."
    ):
        subprocess.run(
            ["python", "Build_Universe_V3.py"]
        )

    st.success(
        "Market Updated"
    )