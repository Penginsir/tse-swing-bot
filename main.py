# main.py  ⭐ 完全オフライン版 ⭐
import datetime as dt
from pathlib import Path
import pandas as pd

# ─────────────────────────────
# 設定
START_CASH = 50_000                     # 初期資金
DATA_DIR   = Path(__file__).with_name("data")   # CSV フォルダ
UNIVERSE   = [p.stem for p in DATA_DIR.glob("*.csv")]  # data/*.csv すべて
# ─────────────────────────────

def fetch_price(code: str) -> pd.Series:
    """CSV から終値 Series を返す"""
    fp = DATA_DIR / f"{code}.csv"
    df = pd.read_csv(fp, parse_dates=["Date"])
    return df.set_index("Date")["Close"]

def strategy_momentum(px: pd.Series) -> int:
    """20日と60日 SMA クロス: 買い=+1, 売り=-1, それ以外=0"""
    sma20 = px.rolling(20).mean().iloc[-1]
    sma60 = px.rolling(60).mean().iloc[-1]
    if sma20 > sma60:
        return 1
    elif sma20 < sma60:
        return -1
    return 0

def main():
    today = dt.date.today()
    buys  = []

    # 1. シグナル生成
    for code in UNIVERSE:
        sig = strategy_momentum(fetch_price(code))
        if sig == 1:
            buys.append(code)

    # 2. ポジションサイズ計算（等金額）
    cash_each = START_CASH / max(len(buys), 1)

    # 3. 発注リスト出力
    print("── 推奨オーダー ──")
    for code in buys:
        last_px = fetch_price(code).iloc[-1]
        qty     = int(cash_each // last_px // 100) * 100  # 最低100株単位
        if qty:
            price = round(last_px * 0.997)                # 指値＝終値-0.3%
            print(f"{code}  買い  指値{price}円  {qty}株")
    print("--------------------")
    print(f"実行日: {today}")

if __name__ == "__main__":
    main()

