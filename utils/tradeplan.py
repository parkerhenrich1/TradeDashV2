import math


def calculate_trade_plan(
    entry,
    atr,
    account_size,
    risk_pct
):

    stop = round(
        entry - (atr * 3),
        2
    )

    risk_per_share = max(
        entry - stop,
        0.01
    )

    risk_amount = (
        account_size
        *
        (risk_pct / 100)
    )

    shares = math.floor(
        risk_amount
        /
        risk_per_share
    )

    target2 = round(
        entry
        + risk_per_share * 2,
        2
    )

    target3 = round(
        entry
        + risk_per_share * 3,
        2
    )

    return {
        "stop": stop,
        "target2": target2,
        "target3": target3,
        "shares": shares
    }
