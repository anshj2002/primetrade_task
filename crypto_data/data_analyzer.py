import pandas as pd

def analyze_data(data):
    df = pd.DataFrame(data)

    
    top_5_by_market_cap = df.nlargest(5, 'market_cap')[['name', 'symbol','market_cap']]
    average_price = df['current_price'].mean()
    
    highest_change = df.nlargest(1, 'price_change_24h')[['name', 'price_change_24h']]
    lowest_change = df.nsmallest(1, 'price_change_24h')[['name', 'price_change_24h']]

    highest_change.rename(columns={"price_change_24h": "change"}, inplace=True)
    lowest_change.rename(columns={"price_change_24h": "change"}, inplace=True)

    return {
        "top_5_by_market_cap": top_5_by_market_cap.to_dict(orient='records'),
        "average_price_top_50": average_price,
        "highest_24h_change": highest_change.to_dict(orient='records')[0],
        "lowest_24h_change": lowest_change.to_dict(orient='records')[0],
    }
