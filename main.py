# main.py
import datetime as dt
import yfinance as yf
import pandas as pd

START_CASH = 50_000  # 初期資金

def fetch_price(code, period="3mo"):
    return yf.download(f"{code}.T", period=period)["Close"]

def strategy_momentum(px):
    sma20 = px.rolling(20).mean().iloc[-1]
    sma60 = px.rolling(60).mean().iloc[-1]
    if sma20 > sma60:
        return 1   # 買い
    elif sma20 < sma60:
        return -1  # 売り
    return 0       # 何もしない

def main():
    today = dt.date.today()
    universe = ["8518", "8918", "8914"]  # 単価が安いサンプル銘柄
    signals, picks = {}, []

    for code in universe:
        px = fetch_price(code)
        sig = strategy_momentum(px)
        signals[code] = sig
        if sig == 1:
            picks.append(code)

    cash_each = START_CASH / max(len(picks), 1)

    print("── 推奨オーダー ──")
    for code in picks:
        last_px = fetch_price(code, "5d").iloc[-1]
        qty = int(cash_each // last_px // 100) * 100  # 最低100株
        if qty:
            price = round(last_px * 0.997)             # 指値＝終値-0.3%
            print(f"{code}  買い  指値 {price}円  {qty}株")
    print("--------------------")
    print(f"実行日: {today}")

if __name__ == "__main__":
    main()
