from flask import Blueprint, jsonify, current_app
from flask import render_template
import concurrent.futures
import requests

main = Blueprint('main', __name__)

def fetch_quote_and_profile(symbol, api_key, base_url):
    quote_url = f"{base_url}/quote"
    profile_url = f"{base_url}/stock/profile2"
    params = {"symbol": symbol, "token": api_key}

    quote_resp = requests.get(quote_url, params=params)
    profile_resp = requests.get(profile_url, params=params)

    if quote_resp.status_code == 200 and profile_resp.status_code == 200:
        data = quote_resp.json()
        profile = profile_resp.json()
        return symbol, {
            "quote": data,
            "logo": profile.get("logo", ""),
            "name": profile.get("name", ""),
        }
    else:
        return symbol, {"error": "Failed to fetch"}

def fetch_quotes_with_logo(symbols, api_key, base_url):
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_quote_and_profile, symbol, api_key, base_url) for symbol in symbols]

        for future in concurrent.futures.as_completed(futures):
            symbol, data = future.result()
            results[symbol] = data

    return results

@main.route('/api/stock')
def get_quotes():
    api_key = current_app.config['FINNHUB_API_KEY']
    base_url = current_app.config['BASE_URL']
    symbols = ["ACHR","INTC","NVDA","AEO","ASTS"]
    data = fetch_quotes_with_logo(symbols, api_key, base_url)
    return jsonify(data)

@main.route('/')
def index():
    return render_template('index.html')
