import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    BASE_URL = "https://finnhub.io/api/v1"