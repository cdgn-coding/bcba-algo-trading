continuous_features = [
    'Open', 'High', 'Low', 'Close', 'Volume',
    'MACD', 'RSI', 'BB_High', 'BB_Mid', 'BB_Low',
    'ATR', 'NATR', 'Currency_Volume', 'Adj Close'
]
categorical_features = ['Month', 'Weekday', 'Ticker', 'Currency']
features = continuous_features + categorical_features