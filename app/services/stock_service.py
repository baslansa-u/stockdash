import requests
from config import Config

def fetch_quotes(symbols):
    results = {}
    for symbol in symbols:
        url = f"{Config.BASE_URL}/quote"
        params = {
            "symbol": symbol,
            "token": Config.FINNHUB_API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results[symbol] = response.json()
        else:
            results[symbol] = {"error": "Failed to fetch"}
    return results
