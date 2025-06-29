import pandas as pd, yfinance as yf, pathlib, io, requests, time

DEST = pathlib.Path(__file__).parent.parent / "data"
DEST.mkdir(exist_ok=True)

# JPX 公開の上場会社一覧 CSV
URL = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq00000030ng-att/data_j.csv"
df = pd.read_csv(io.BytesIO(requests.get(URL).content))

codes = (
    df["コード"].astype(str).str.zfill(4).unique().tolist()
)

for code in codes:
    try:
        price = yf.download(f"{code}.T", period="6mo", interval="1d", progress=False)
        if not price.empty:
            price.to_csv(DEST / f"{code}.csv")
    except Exception as e:
        print(f"skip {code}: {e}")
    time.sleep(0.3)   # アクセス制限対策、約 20 分で完了
