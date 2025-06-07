# backend/stocks.py

from fastapi import APIRouter
from backend.scraper import fetch_all_stocks

router = APIRouter()

@router.get("/stocks")
def read_stocks():
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    data = fetch_all_stocks(symbols)
    return {"stocks": data}
