CREATE KEYSPACE IF NOT EXISTS binance
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE binance;

-- Latest Prices
CREATE TABLE IF NOT EXISTS latest_prices (
    symbol TEXT,
    price TEXT,
    fetched_at TIMESTAMP,
    PRIMARY KEY (symbol, fetched_at)
);

-- Recent Trades
CREATE TABLE IF NOT EXISTS recent_trades (
    id BIGINT,
    price TEXT,
    qty TEXT,
    quote_qty TEXT,
    time BIGINT,
    is_buyer_maker BOOLEAN,
    is_best_match BOOLEAN,
    fetched_at TIMESTAMP,
    symbol TEXT,
    PRIMARY KEY (id, symbol)
);

-- Candlesticks (15m)
CREATE TABLE IF NOT EXISTS candlesticks_15m (
    open_time BIGINT,
    open_price TEXT,
    high_price TEXT,
    low_price TEXT,
    close_price TEXT,
    volume TEXT,
    close_time BIGINT,
    quote_asset_volume TEXT,
    no_trades BIGINT,
    base_asset_volume TEXT,
    buy_quote_asset_volume TEXT,
    unused TEXT,
    fetched_at TIMESTAMP,
    symbol TEXT,
    PRIMARY KEY (symbol, open_time)
);

-- Ticker Stats (24h)
CREATE TABLE IF NOT EXISTS ticker_stats_24h (
    symbol TEXT,
    price_change TEXT,
    price_change_percent TEXT,
    weighted_avg_price TEXT,
    prev_close_price TEXT,
    last_price TEXT,
    last_qty TEXT,
    bid_price TEXT,
    bid_qty TEXT,
    ask_price TEXT,
    ask_qty TEXT,
    open_price TEXT,
    high_price TEXT,
    low_price TEXT,
    volume TEXT,
    quote_volume TEXT,
    open_time BIGINT,
    close_time BIGINT,
    first_id BIGINT,
    last_id BIGINT,
    count BIGINT,
    fetched_at TIMESTAMP,
    PRIMARY KEY (symbol, fetched_at)
);

-- Order Book Bids
CREATE TABLE IF NOT EXISTS orderbook_bids (
    symbol TEXT,
    price TEXT,
    quantity TEXT,
    fetched_at TIMESTAMP,
    PRIMARY KEY (symbol, fetched_at, price)
);

-- Order Book Asks
CREATE TABLE IF NOT EXISTS orderbook_asks (
    symbol TEXT,
    price TEXT,
    quantity TEXT,
    fetched_at TIMESTAMP,
    PRIMARY KEY (symbol, fetched_at, price)
);
