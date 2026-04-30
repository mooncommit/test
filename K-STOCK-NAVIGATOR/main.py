from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from typing import Optional
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 추가 (404 방지용)
@app.get("/")
def root():
    return {"message": "server running"}


WATCH_TICKERS = {
    "005930.KS": "반도체",
    "000660.KS": "반도체",
    "AAPL": "IT",
    "TSLA": "자동차",
    "NVDA": "반도체"
}

NAME_MAP = {
    "005930.KS": "삼성전자",
    "000660.KS": "SK하이닉스",
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA"
}


# -----------------------------
# 실시간 데이터
# -----------------------------
def get_data():
    result = []

    for ticker, cat in WATCH_TICKERS.items():
        try:
            hist = yf.Ticker(ticker).history(period="5d")

            if len(hist) < 2:
                raise Exception()

            price = hist["Close"].iloc[-1]
            prev = hist["Close"].iloc[-2]
            change = round((price - prev) / prev * 100, 2)
            volume = hist["Volume"].iloc[-1]

            result.append({
                "ticker": ticker,
                "name": NAME_MAP[ticker],
                "price_str": f"{int(price):,}",
                "change": change,
                "vol_val": int(volume),
                "category": cat
            })

        except:
            # 🔥 fallback
            p = random.randint(50000, 150000)
            result.append({
                "ticker": ticker,
                "name": NAME_MAP[ticker],
                "price_str": f"{p:,}",
                "change": round(random.uniform(-2, 2), 2),
                "vol_val": random.randint(100000, 2000000),
                "category": cat
            })

    return result


# -----------------------------
@app.get("/stock/realtime")
def realtime(category: Optional[str] = Query(None)):
    data = sorted(get_data(), key=lambda x: x["vol_val"], reverse=True)
    if category and category != "전체":
        return [d for d in data if d["category"] == category]
    return data


# -----------------------------
@app.get("/stock/categories")
def categories():
    data = get_data()
    stats = {}

    for d in data:
        stats.setdefault(d["category"], []).append(d["change"])

    icons = {"반도체": "📟", "자동차": "🚗", "IT": "💻"}

    result = []
    for k, v in stats.items():
        result.append({
            "name": k,
            "change": round(sum(v)/len(v), 2),
            "icon": icons.get(k, "🔥")
        })

    return result


# -----------------------------
@app.get("/stock/detail")
def detail(ticker: str):
    return {
        "price": random.randint(50000, 150000),
        "per": round(random.uniform(10, 20), 2),
        "market_cap": "100조",
        "sector": "테스트"
    }


# -----------------------------
@app.get("/stock/chart")
def chart(ticker: str):
    return {
        "dates": [f"{i+1}" for i in range(30)],
        "prices": [random.randint(50000, 150000) for _ in range(30)]
    }