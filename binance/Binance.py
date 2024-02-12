import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from private import private_key
from constants import constants
import RsaEnDecrypt

import ccxt
import pandas as pd

class Binance:
    def __init__(self):
        RSA = private_key.RSA
        
        rsa_decrypt = RsaEnDecrypt.RsaEnDecrypt(RSA['ENCRYPT_KEY'])
        BINANCE_ACCESS = rsa_decrypt.decrypt(RSA['ACCESS'])
        BINANCE_SECRET = rsa_decrypt.decrypt(RSA['SECRET'])

        self.binance = ccxt.binance(config={
            'apiKey': BINANCE_ACCESS,
            'secret': BINANCE_SECRET,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })

        self.balance = self.binance.fetch_balance(params={"type": "future"})

    def get_balance(self):
        return self.balance


    def get_top_volume_ticker_list(self, ticker_cnt):
        tickers = self.binance.fetch_tickers()
        dic_ticker_volume = dict()

        for ticker in tickers:
            try:
                if "/USDT" in ticker:
                    dic_ticker_volume[ticker] = tickers[ticker]['baseVolume'] * \
                        tickers[ticker]['close']
            except Exception as e:
                print("---:", e)

        dic_sorted_ticker_volume = sorted(
            dic_ticker_volume.items(), key=lambda x: x[1], reverse=True)

        ticker_list = list()
        cnt = 0

        for ticker in dic_sorted_ticker_volume:
            # only get USDT ticker
            if "/USDT" not in ticker[0]:
                continue
            
            # exception for banned tickers
            BANNED_TICKERS = constants.SETTING['TICKER']['BANNED']
            if ticker in BANNED_TICKERS:
                continue

            cnt += 1
            if cnt <= ticker_cnt:
                ticker_list.append(ticker[0])
            else:
                break

        return ticker_list


    # period: (1d,4h,1h,15m,10m,1m ...)
    def get_ohlcv(self, ticker, period):
        binance_ohlcv = self.binance.fetch_ohlcv(ticker, period)

        ohlcv = pd.DataFrame(binance_ohlcv,columns=[
            'datetime', 'open',
            'high', 'low',
            'close', 'volume'
        ])

        ohlcv['datetime'] = pd.to_datetime(ohlcv['datetime'], unit='ms')
        ohlcv.set_index('datetime', inplace=True)

        return ohlcv

    def get_min_amount(self, ticker):
        limit_values = self.binance.markets[ticker]['limits']

        min_amount = limit_values['amount']['min']
        min_cost = limit_values['cost']['min']
        min_price = limit_values['price']['min']

        ticker_info = self.binance.fetch_ticker(ticker)
        coin_price = ticker_info['last']

        print(f"| Coin_price : {coin_price} $")
        # print(f"| min_cost : {min_cost} $ -> min_amount")
        # print(f"| min_amount : {min_amount} EA")
        # print(f"| min_price : {min_price} $")

        # get mininum unit price to be able to order
        if min_price < coin_price:
            min_price = coin_price

        # order cost = price * amount
        min_order_cost = min_price * min_amount

        multiple_cnt = 1

        if min_cost is not None and min_order_cost < min_cost:
            # if min_order_cost is smaller than min cost
            # increase the min_order_cost bigger than min cost
            # by the multiple multiple_cnt of minimum amount
            while min_order_cost < min_cost:
                multiple_cnt += 1
                min_order_cost = min_price * (multiple_cnt * min_amount)

        minimum_amount = multiple_cnt * min_amount

        return (min_order_cost, minimum_amount)

    def get_ticker_current_price(self, ticker):
        ticker_info = self.binance.fetch_ticker(ticker)
        coin_price = ticker_info['last']  # coin_info['close'] == coin_info['last']

        return coin_price