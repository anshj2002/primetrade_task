import os
from dotenv import load_dotenv

load_dotenv()

API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
API_KEY = os.getenv('COIN_MARKET_CAP_API_KEY')



API_PARAMETERS = {
    'start': '1',
    'limit': '50',
    'convert': 'USD',
}
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}
