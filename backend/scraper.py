# backend/scraper.py

import yfinance as yf
from typing import Dict

def fetch_stock_data(symbol: str) -> Dict:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        return {
            "symbol": symbol,
            "price": info.get("regularMarketPrice"),
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "roe": info.get("returnOnEquity"),
            "dividend_yield": info.get("dividendYield"),
            "market_cap": info.get("marketCap"),
            "beta": info.get("beta"),
            "volatility": info.get("52WeekChange"),  # Simplified proxy
        }
    except Exception as e:
        return {"error": str(e)}
def get_stock_data(ticker: str) -> dict:
    import yfinance as yf

    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker,
        "price": info.get("currentPrice"),
        "pe_ratio": info.get("trailingPE"),
        "eps": info.get("trailingEps"),
        "roe": info.get("returnOnEquity"),
        "dividend_yield": info.get("dividendYield"),
        "market_cap": info.get("marketCap"),
        "beta": info.get("beta"),
        "volatility": info.get("fiftyTwoWeekHigh") - info.get("fiftyTwoWeekLow"),
    }


def fetch_all_stocks(symbols: list[str]) -> list[Dict]:
    return [fetch_stock_data(sym) for sym in symbols]

# Example usage (if needed in testing):
if __name__ == "__main__":
    symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA"]
    for data in fetch_all_stocks(symbols):
        print(data)
