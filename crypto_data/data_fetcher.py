import requests
import json
from config import API_URL, API_PARAMETERS, HEADERS
import time
import pandas as pd
from datetime import datetime

data_cache={
    "data": None,
    "timestamp": None
}


def extract_cryptocurrency_data(data):
    extracted_data = []
    for crypto in data:
        extracted_data.append({
            "name": crypto["name"],
            "symbol": crypto["symbol"],
            "current_price": crypto["quote"]["USD"]["price"],
            "market_cap": crypto["quote"]["USD"]["market_cap"],
            "volume_24h": crypto["quote"]["USD"]["volume_24h"],
            "price_change_24h": crypto["quote"]["USD"]["percent_change_24h"],
        })

    df = pd.DataFrame(extracted_data)
    df = df.sort_values(by=['market_cap','current_price'], ascending=False)
    
    return df


def fetch_crypto_data():
    try:

        
        if data_cache["data"] and time.time() - data_cache["timestamp"] < 300:
            print("Using cached data")
            cached_result = extract_cryptocurrency_data(data_cache["data"]) 
            readable_timestamp = datetime.fromtimestamp(data_cache["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')

            return [cached_result , readable_timestamp]


        print("Fetching crypto data...")
        
        response = requests.get(API_URL, headers=HEADERS, params=API_PARAMETERS)
        response.raise_for_status()
        data = response.json()
        
        data_cache["data"] = data["data"]
        data_cache["timestamp"] = time.time()
        
        result = extract_cryptocurrency_data(data['data'])
        readable_timestamp = datetime.fromtimestamp(data_cache["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')

        return [result , readable_timestamp]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
