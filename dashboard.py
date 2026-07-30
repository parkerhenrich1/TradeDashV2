import streamlit as st

from utils.data_loader import load_data
from utils.market import calculate_market_regime


def show_dashboard():

    (
        rankings,
        indicators,
        elite,
        institutional,
        journal
    ) = load_data()

    (
        market_regime,
        spy_close,
        spy_sma200,
        spy_return
    ) = calculate_market_regime()

    hc = len(
        rankings[
            rankings["AlphaScore"] >= 95
        ]
    )

    avg_alpha = round(
        rankings["AlphaScore"]
        .head(100)
        .mean(),
        1
    )

    elite_signals = len(
        rankings[
            rankings["AlphaScore"] >= 95
        ]
    )

    watch_signals = len(
        rankings[
            rankings["AlphaScore"] >= 90
        ]
    )

    st.header(
        "📈 TradeDash Dashboard"
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric(
        "Market",
        market_regime
    )

    c2.metric(
        "SPY",
        round(spy_close, 2)
        if spy_close == spy_close
        else "N/A"
    )

    c3.metric(
        "Top20 Alpha",
        avg_alpha
    )

    c4.metric(
        "Elite Signals",
        elite_signals
    )

    c5.metric(
        "Watch Signals",
        watch_signals
    )

    c6.metric(
        "High Conviction",
        hc
    )

    st.divider()

    st.subheader(
        "Top Ranked Stocks"
    )

    display_cols = [
        col for col in [
            "Rank",
            "Symbol",
            "AlphaScore",
            "Return3M",
            "RVOL",
            "Decision"
        ]
        if col in rankings.columns
    ]

    st.dataframe(
        rankings[
            display_cols
        ].head(20),
        use_container_width=True
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader(
            "🏆 Elite Leaders"
        )

        st.metric(
            "Total Elite Leaders",
            len(elite)
        )

        st.dataframe(
            elite.head(20),
            use_container_width=True
        )

    with right:

        st.subheader(
            "🏦 Institutional Accumulation"
        )

        st.metric(
            "Institutional Candidates",
            len(institutional)
        )

        st.dataframe(
            institutional.head(20),
            use_container_width=True
        )

    st.divider()

    st.subheader(
        "Market Health"
    )

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Market Regime",
        market_regime
    )

    m2.metric(
        "SPY Close",
        round(spy_close, 2)
        if spy_close == spy_close
        else "N/A"
    )

    m3.metric(
        "SPY SMA200",
        round(spy_sma200, 2)
        if spy_sma200 == spy_sma200
        else "N/A"
    )

    if market_regime == "BULL":

        st.success(
            "✅ Market is above the 200-day moving average. BUY signals are enabled."
        )

    elif market_regime == "BEAR":

        st.warning(
            "⚠️ Market is below the 200-day moving average. BUY signals are downgraded to WATCH."
        )

    else:

        st.info(
            "Market regime unavailable."
        )