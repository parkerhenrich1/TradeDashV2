import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
from datetime import datetime


@st.cache_data(ttl=3600)
def calculate_market_regime():

    try:

        spy = yf.download(
            "SPY",
            period="2y",
            auto_adjust=True,
            progress=False
        )

        if spy.empty:
            raise ValueError(
                "No SPY data returned"
            )

        if isinstance(
            spy.columns,
            pd.MultiIndex
        ):
            spy.columns = (
                spy.columns
                .get_level_values(0)
            )

        spy["SMA200"] = (
            spy["Close"]
            .rolling(200)
            .mean()
        )

        spy_close = float(
            spy["Close"].iloc[-1]
        )

        spy_sma200 = float(
            spy["SMA200"].iloc[-1]
        )

        spy_return_3m = (
            (
                spy_close
                /
                float(
                    spy["Close"]
                    .iloc[-63]
                )
            )
            - 1
        ) * 100

        regime = (
            "BULL"
            if spy_close > spy_sma200
            else "BEAR"
        )

        return (
            regime,
            spy_close,
            spy_sma200,
            spy_return_3m
        )

    except Exception as e:

        st.error(
            f"SPY Error: {e}"
        )

        return (
            "UNKNOWN",
            np.nan,
            np.nan,
            np.nan
        )

def calculate_relative_strength(
    stock_return,
    spy_return
):

    try:
        return round(
            stock_return - spy_return,
            2
        )

    except:

        return np.nan


def get_earnings_info(ticker):

    try:

        stock = yf.Ticker(ticker)

        calendar = stock.calendar

        if calendar is None:
            return None, None

        earnings = pd.to_datetime(
            calendar.iloc[0][0]
        ).date()

        days = (
            earnings
            - datetime.today().date()
        ).days

        return earnings, days

    except:

        return None, None