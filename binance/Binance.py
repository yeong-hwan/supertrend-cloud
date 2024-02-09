import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from private import private_key
import RsaEnDecrypt

import ccxt

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

    def get_top_volume_coin_list(self, coin_cnt):
        tickers = self.binance.fetch_tickers()
        dic_coin_money = dict()

        for ticker in tickers:
            try:
                if "/USDT" in ticker:
                    dic_coin_money[ticker] = tickers[ticker]['baseVolume'] * \
                        tickers[ticker]['close']
            except Exception as e:
                print("---:", e)

        dic_sorted_coin_money = sorted(
            dic_coin_money.items(), key=lambda x: x[1], reverse=True)

        coin_list = list()
        cnt = 0

        for coin_data in dic_sorted_coin_money:
            cnt += 1
            if cnt <= coin_cnt:
                coin_list.append(coin_data[0])
            else:
                break

        return coin_list
