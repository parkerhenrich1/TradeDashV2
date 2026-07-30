import math
import streamlit as st


def show_risk_calculator():

    st.header(
        "Risk Calculator"
    )

    acct = st.number_input(
        "Account Size",
        value=10000.0
    )

    risk_pct = st.number_input(
        "Risk %",
        value=1.0
    )

    entry = st.number_input(
        "Entry",
        value=100.0
    )

    stop = st.number_input(
        "Stop",
        value=95.0
    )

    risk_amt = (
        acct
        * (risk_pct / 100)
    )

    rps = (
        entry
        - stop
    )

    shares = (
        math.floor(
            risk_amt / rps
        )
        if rps > 0
        else 0
    )

    st.metric(
        "Position Size",
        shares
    )

    st.metric(
        "Risk Amount",
        round(risk_amt, 2)
    )
