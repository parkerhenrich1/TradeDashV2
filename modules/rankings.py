import streamlit as st

from utils.data_loader import load_data


def show_rankings():

    (
        rankings,
        indicators,
        elite,
        institutional,
        journal
    ) = load_data()

    st.subheader(
        "Full Rankings"
    )

    st.dataframe(
        rankings,
        use_container_width=True
    )
