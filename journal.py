import pandas as pd
import streamlit as st


def show_journal():

    st.header(
        "📒 Trade Journal"
    )

    try:

        journal_df = pd.read_csv(
            "trade_journal.csv"
        )

        st.metric(
            "Total Trades",
            len(journal_df)
        )

        st.dataframe(
            journal_df,
            use_container_width=True
        )

    except Exception:

        st.info(
            "No journal entries yet."
        )