import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from private import private_key
import RsaEnDecrypt

import ccxt
import pandas as pd

class Binance:
    def __init__(self):
        rsa_decrypt = RsaEnDecrypt.RsaEnDecrypt(private_key.RSA['ENCRYPT_KEY'])
        BINANCE_ACCESS = rsa_decrypt.decrypt(private_key.RSA['ACCESS'])
        BINANCE_SECRET = rsa_decrypt.decrypt(private_key.RSA['SECRET'])

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
            BANNED_TICKERS = constants.TICKER['BANNED']
            if ticker in BANNED_TICKERS:
                continue

            cnt += 1
            if cnt <= ticker_cnt:
                ticker_list.append(ticker[0])
            else:
                break

        return ticker_list

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