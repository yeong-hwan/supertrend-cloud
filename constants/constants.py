BINANCE = {
    "LEVERAGE": 3,
    "IS_ISOLATED": True
}

PATH = {
    # "SERVER": "/var/trading-bot/positioned_list.json",
    "LOCAL": "log/positioned_list.json"
}

TICKER = {
    "BANNED": [
        "SRM/USDT",
        "FTT/USDT"
    ],
    "TICKER_COUNT": 10
}

STATE = {
    "CLOUD"
}

SUPERTREND_SETTING = {
    "5M": {
        "PERIOD_1": 6,
        "MULTIPLIER_1": 10,
        "PERIOD_2": 10,
        "MULTIPLIER_2": 6
    },
    "4H": {
        "PERIOD_1": 10,
        "MULTIPLIER_1": 3,
        "PERIOD_2": 10,
        "MULTIPLIER_2": 6
    },
    "BTC_4H": {
        "PERIOD_1": 4,
        "MULTIPLIER_1": 2.4,
        "PERIOD_2": 4,
        "MULTIPLIER_2": 4.8
    }
}

# print(SUPERTREND_SETTING['5M']['PERIOD'])