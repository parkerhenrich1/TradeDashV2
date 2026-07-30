import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from plotly.subplots import make_subplots

from utils.data_loader import load_data

from utils.market import (
    calculate_market_regime,
    calculate_relative_strength,
    get_earnings_info
)

from utils.signals import (
    calculate_reclaim20,
    calculate_signal_score,
    get_rating
)

from utils.tradeplan import (
    calculate_trade_plan
)


def show_research():

    (
        rankings,
        indicators,
        elite,
        institutional,
        journal
    ) = load_data()

    st.subheader("Research Terminal")

    ticker = st.selectbox(
        "Ticker",
        sorted(rankings["Symbol"].unique())
    )

    stock = rankings[
        rankings["Symbol"] == ticker
    ].iloc[0]

    price = float(stock["Price"])
    alpha = float(stock["AlphaScore"])
    ret3m = float(stock["Return3M"])
    rvol = float(stock["RVOL"])
    dist52 = float(stock["Dist52High"])
    
    (
        market_regime,
        spy_close,
        spy_sma200,
        spy_return_3m
    ) = calculate_market_regime()
    
    st.write(
        "DEBUG:",
        market_regime,
        spy_close,
        spy_sma200,
        spy_return_3m
    )

    rs_value = calculate_relative_strength(
        ret3m,
        spy_return_3m
    )

    earnings_date, days_to_earnings = (
        get_earnings_info(ticker)
    )

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric(
        "AlphaScore",
        int(alpha)
    )

    m2.metric(
        "Return3M",
        round(ret3m, 2)
    )

    m3.metric(
        "RVOL",
        round(rvol, 2)
    )

    m4.metric(
        "RS vs SPY",
        round(rs_value, 2)
    )

    m5.metric(
        "Market",
        market_regime
    )

    st.divider()

    period = st.selectbox(
        "Timeframe",
        ["6mo", "1y", "2y", "5y"],
        index=1
    )

    indicators_selected = st.multiselect(
        "Indicators",
        [
            "SMA20",
            "SMA50",
            "SMA200",
            "Kijun",
            "VWAP"
        ],
        default=[
            "SMA20",
            "SMA50",
            "SMA200"
        ]
    )

    data = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if data.empty:

        st.error(
            "Unable to download market data."
        )

        return

    close = data["Close"]

    data["SMA20"] = close.rolling(20).mean()
    data["SMA50"] = close.rolling(50).mean()
    data["SMA200"] = close.rolling(200).mean()

    data["Kijun"] = (
        (
            data["High"].rolling(26).max()
            +
            data["Low"].rolling(26).min()
        ) / 2
    )

    data["VWAP"] = (
        (
            close * data["Volume"]
        ).cumsum()
        /
        data["Volume"].cumsum()
    )

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rs_calc = (
        gain.rolling(14).mean()
        /
        loss.rolling(14).mean()
    )

    data["RSI"] = (
        100
        -
        (
            100
            /
            (1 + rs_calc)
        )
    )

    tr1 = data["High"] - data["Low"]

    tr2 = (
        data["High"]
        - data["Close"].shift()
    ).abs()

    tr3 = (
        data["Low"]
        - data["Close"].shift()
    ).abs()

    data["ATR"] = (
        pd.concat(
            [tr1, tr2, tr3],
            axis=1
        )
        .max(axis=1)
        .rolling(14)
        .mean()
    )

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        row_heights=[
            0.65,
            0.20,
            0.15
        ]
    )

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Price"
        ),
        row=1,
        col=1
    )

    for indicator in indicators_selected:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[indicator],
                name=indicator
            ),
            row=1,
            col=1
        )

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume"
        ),
        row=2,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["RSI"],
            name="RSI"
        ),
        row=3,
        col=1
    )

    fig.update_layout(
        template="plotly_dark",
        height=900
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    current_close = float(
        data["Close"].iloc[-1]
    )

    current_sma200 = float(
        data["SMA200"].iloc[-1]
    )

    elite_leader = (
        alpha >= 95
        and ret3m >= 50
        and rvol >= 1.5
        and dist52 >= -3
    )

    reclaim20 = calculate_reclaim20(
        data
    )

    signal_score = (
        calculate_signal_score(
            alpha,
            ret3m,
            rvol,
            dist52,
            reclaim20,
            rs_value,
            market_regime
        )
    )

    signal_rating = get_rating(
        signal_score
    )

    buy_signal = (
        elite_leader
        and reclaim20
        and rs_value > 20
        and market_regime == "BULL"
    )

    if (
        days_to_earnings is not None
        and days_to_earnings < 5
    ):
        buy_signal = False

    score_pct = round(
        (signal_score / 7) * 100,
        1
    )

    st.subheader(
        "🎯 TradeDash Signal"
    )

    if buy_signal:

        st.success(
            f"BUY | {signal_rating}"
        )

    elif signal_score >= 5:

        st.warning(
            f"WATCH | {signal_rating}"
        )

    else:

        st.error(
            f"AVOID | {signal_rating}"
        )

    a, b, c = st.columns(3)

    a.metric(
        "Signal Score",
        f"{signal_score}/7"
    )

    b.metric(
        "Score %",
        f"{score_pct}%"
    )

    c.metric(
        "Rating",
        signal_rating
    )
    st.subheader("🚪 Exit Decision")

    st.write("Exit section loaded")

    sell_signal = False

    if current_close < current_sma200:

        sell_signal = True
        st.error("❌ Below SMA200")

    if rs_value < 10:

        sell_signal = True
        st.warning("⚠️ Relative Strength Deteriorating")

    if market_regime == "BEAR":

        st.warning("⚠️ Market Regime Bearish")

    if not sell_signal:

        st.success(
            "✅ Continue Holding"
        )
        
    st.subheader(
        "Trade Quality Assessment"
    )

    q1, q2, q3, q4, q5 = st.columns(5)

    q1.metric(
        "Trend",
        "GOOD"
        if current_close > current_sma200
        else "RISK"
    )

    q2.metric(
        "RS",
        "GOOD"
        if rs_value > 20
        else "NEUTRAL"
    )

    q3.metric(
        "Volume",
        "GOOD"
        if rvol > 1.5
        else "NEUTRAL"
    )

    q4.metric(
        "Market",
        market_regime
    )

    q5.metric(
        "Earnings",
        (
            "RISK"
            if (
                days_to_earnings is not None
                and days_to_earnings < 5
            )
            else "CLEAR"
        )
    )

    st.subheader(
        "Trade Plan"
    )

    account_size = st.number_input(
        "Account Size",
        value=25000.0
    )

    risk_pct = st.number_input(
        "Risk %",
        value=1.0
    )

    atr = float(
        data["ATR"].iloc[-1]
    )

    plan = calculate_trade_plan(
        current_close,
        atr,
        account_size,
        risk_pct
    )

    p1, p2, p3, p4, p5 = st.columns(5)

    p1.metric(
        "Entry",
        round(current_close, 2)
    )

    p2.metric(
        "ATR Stop",
        plan["stop"]
    )

    p3.metric(
        "2R Target",
        plan["target2"]
    )

    p4.metric(
        "3R Target",
        plan["target3"]
    )

    p5.metric(
        "Position Size",
        plan["shares"]
    )

    st.divider()

    st.subheader(
        "📒 Add To Journal"
    )

    notes = st.text_area(
        "Trade Notes",
        height=100
    )

    if st.button(
        "➕ Add To Journal"
    ):

        new_trade = pd.DataFrame([
            {
                "Date": pd.Timestamp.now().date(),
                "Symbol": ticker,
                "AlphaScore": alpha,
                "Return3M": ret3m,
                "RVOL": rvol,
                "RS": rs_value,
                "SignalScore": signal_score,
                "EntryPrice": current_close,
                "StopPrice": plan["stop"],
                "TargetPrice": plan["target3"],
                "Notes": notes
            }
        ])

        try:

            journal_df = pd.read_csv(
                "trade_journal.csv"
            )

            journal_df = pd.concat(
                [
                    journal_df,
                    new_trade
                ],
                ignore_index=True
            )

        except Exception:

            journal_df = new_trade

        journal_df.to_csv(
            "trade_journal.csv",
            index=False
        )

        st.success(
            f"{ticker} added to journal"
        )

    tv_url = (
        f"https://www.tradingview.com/symbols/NASDAQ-{ticker}/"
    )

    st.link_button(
        f"📊 Open {ticker} in TradingView",
        tv_url
    )
