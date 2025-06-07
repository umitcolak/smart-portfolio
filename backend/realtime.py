# backend/realtime.py

import asyncio
import yfinance as yf
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

router = APIRouter()

# Symbols to track
TRACKED_SYMBOLS = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA"]

# Connected clients
clients: List[WebSocket] = []

# Metrics split by volatility
DYNAMIC_KEYS = ["regularMarketPrice", "marketCap"]
STATIC_KEYS = [
    "trailingPE", "trailingEps", "returnOnEquity", "dividendYield", "beta", "52WeekChange"
]

# Fetch dynamic data (frequent)
def fetch_dynamic(symbol: str) -> Dict:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        price = info.get("regularMarketPrice")
        shares_out = info.get("sharesOutstanding") or 1
        return {
            "symbol": symbol,
            "price": price,
            "market_cap": price * shares_out,
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}

# Fetch static data (occasional)
def fetch_static(symbol: str) -> Dict:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "symbol": symbol,
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "roe": info.get("returnOnEquity"),
            "dividend_yield": info.get("dividendYield"),
            "beta": info.get("beta"),
            "volatility": info.get("52WeekChange"),
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}

# Cached static info to avoid frequent re-fetching
STATIC_CACHE: Dict[str, Dict] = {}

# WebSocket endpoint
@router.websocket("/ws/prices")
async def stream_prices(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        # Fetch static info once
        for symbol in TRACKED_SYMBOLS:
            STATIC_CACHE[symbol] = fetch_static(symbol)

        while True:
            response = []
            for symbol in TRACKED_SYMBOLS:
                dynamic = fetch_dynamic(symbol)
                static = STATIC_CACHE.get(symbol, {})
                merged = {**dynamic, **static}
                response.append(merged)

            for client in clients:
                await client.send_json({"stocks": response})

            await asyncio.sleep(3)

    except WebSocketDisconnect:
        clients.remove(websocket)
    except Exception as e:
        await websocket.close()
        if websocket in clients:
            clients.remove(websocket)
