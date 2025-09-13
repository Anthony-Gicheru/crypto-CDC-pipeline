import requests
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime, timezone

load_dotenv()

db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')


print(f"🔎 Connection string: postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

BASE_URL = "https://api.binance.com"
TOP_PAIRS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
INTERVAL = '15m'

def save_to_postgres(df, table_name):
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Saved {len(df)} rows to PostgreSQL table: {table_name}")
    except Exception as e:
        print(f" Error saving to {table_name}: {e}")

def get_latest_prices(symbol):
    url = f'{BASE_URL}/api/v3/ticker/price'
    response = requests.get(url, params={'symbol': symbol})
    data = response.json()
    df = pd.DataFrame([data])
    df['fetched_at'] = datetime.now(timezone.utc)
    df['symbol'] = symbol
    return df

def order_book(symbol, limit=20):
    url = f'{BASE_URL}/api/v3/depth'
    response = requests.get(url, params={'symbol': symbol, 'limit': limit})
    order_data = response.json()
    bids_df = pd.DataFrame(order_data['bids'], columns=['price', 'quantity'])
    asks_df = pd.DataFrame(order_data['asks'], columns=['price', 'quantity'])
    fetched_at = datetime.now(timezone.utc)
    bids_df['fetched_at'] = fetched_at
    asks_df['fetched_at'] = fetched_at
    bids_df['symbol'] = symbol
    asks_df['symbol'] = symbol
    return bids_df, asks_df

def recent_trades(symbol, limit=20):
    url = f'{BASE_URL}/api/v3/trades'
    response = requests.get(url, params={'symbol': symbol, 'limit': limit})
    trades_data = response.json()
    df = pd.DataFrame(trades_data)
    df['symbol'] = symbol
    df['fetched_at'] = datetime.now(timezone.utc)
    return df

def get_klines(symbol, interval='15m'):
    url = f'{BASE_URL}/api/v3/klines'
    response = requests.get(url, params={'symbol': symbol, 'interval': interval})
    kline_data = response.json()
    df = pd.DataFrame(kline_data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df['fetched_at'] = datetime.now(timezone.utc)
    df['symbol'] = symbol
    return df

def ticker_stats(symbol):
    url = f'{BASE_URL}/api/v3/ticker/24hr'
    response = requests.get(url, params={'symbol': symbol})
    ticker_data = response.json()
    df = pd.DataFrame([ticker_data])
    df['fetched_at'] = datetime.now(timezone.utc)
    df['symbol'] = symbol
    return df

# Main loop
for symbol in TOP_PAIRS:
    print(f"\n=== Collecting data for {symbol} ===")

    price_df = get_latest_prices(symbol)
    save_to_postgres(price_df, "latest_prices")

    trades_df = recent_trades(symbol)
    save_to_postgres(trades_df, "recent_trades")

    klines_df = get_klines(symbol)
    save_to_postgres(klines_df, "candlesticks_15m")

    ticker_df = ticker_stats(symbol)
    save_to_postgres(ticker_df, "ticker_stats_24h")

    bids_df, asks_df = order_book(symbol)
    save_to_postgres(bids_df, "orderbook_bids")
    save_to_postgres(asks_df, "orderbook_asks")

    print(f"Completed {symbol}")
