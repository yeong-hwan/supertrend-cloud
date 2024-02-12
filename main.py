from binance import Binance
from alert import DiscordAlertBot
from constants import constants
from util import util

import json
import time
import traceback

binance = Binance.Binance()
balance = binance.get_balance()
SETTING = constants.SETTING

# get positioned list by json file
positioned_list = list()
POSITIONED_FILE_PATH = SETTING['PATH']['LOCAL']

try:
    with open(POSITIONED_FILE_PATH, 'r') as json_file:
        positioned_list = json.load(json_file)

except Exception as e:
    print("\n| Exception by First | Not Positioned\n")

try:
    TICKER_COUNT = SETTING['TICKER']['COUNT']

    ticker_list = binance.get_top_volume_ticker_list(TICKER_COUNT)

    for positioned_ticker_data in positioned_list:
        positioned_ticker = positioned_ticker_data[0]
        if positioned_ticker not in ticker_list:
            ticker_list.append(positioned_ticker)

    time.sleep(0.1)

    # ----------------------------------
    ticker_order = 1

    for ticker in ticker_list:
        print(ticker)
        
        candle_5m = binance.get_ohlcv(ticker, "5m")
        time.sleep(0.02)

        print(util.get_supertrend_cloud(candle_5m, "5m"))

        

except Exception as e:
    print("Exception :", e)
    print(traceback.format_exc())