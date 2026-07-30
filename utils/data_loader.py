import pandas as pd
import streamlit as st

FILE = "TradeDash.xlsx"

@st.cache_data
def load_data():

    rankings = pd.read_excel(
        FILE,
        sheet_name="TradeDashRankings",
        engine="openpyxl"
    )

    indicators = pd.read_excel(
        FILE,
        sheet_name="Indicators",
        engine="openpyxl"
    )

    elite = pd.read_excel(
        FILE,
        sheet_name="EliteLeaders",
        engine="openpyxl"
    )

    institutional = pd.read_excel(
        FILE,
        sheet_name="InstitutionalAccumulation",
        engine="openpyxl"
    )

    journal = pd.read_excel(
        FILE,
        sheet_name="Trade Journal",
        engine="openpyxl"
    )

    return (
        rankings,
        indicators,
        elite,
        institutional,
        journal
    )
