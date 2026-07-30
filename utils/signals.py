def calculate_reclaim20(df):

    try:

        prev_close = float(
            df["Close"].iloc[-2]
        )

        current_close = float(
            df["Close"].iloc[-1]
        )

        sma20 = float(
            df["SMA20"].iloc[-1]
        )

        sma50 = float(
            df["SMA50"].iloc[-1]
        )

        sma200 = float(
            df["SMA200"].iloc[-1]
        )

        return (
            prev_close < sma20
            and current_close > sma20
            and current_close > sma50
            and current_close > sma200
        )

    except:

        return False


def calculate_signal_score(
    alpha,
    ret3m,
    rvol,
    dist52,
    reclaim20,
    rs,
    market_regime
):

    score = 0

    score += int(alpha >= 95)
    score += int(ret3m >= 50)
    score += int(rvol >= 1.5)
    score += int(dist52 >= -3)
    score += int(reclaim20)
    score += int(rs > 20)
    score += int(market_regime == "BULL")

    return score


def get_rating(score):

    if score == 7:
        return "★★★★★ Elite"

    elif score == 6:
        return "★★★★ Strong"

    elif score == 5:
        return "★★★ Watchlist"

    return "Avoid"
