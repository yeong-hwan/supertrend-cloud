import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from private import private_key
import RsaEnDecrypt

import ccxt

class Binance:
    def __init__(self):
        rsa_decrypt = RsaEnDecrypt.RsaEnDecrypt(private_key.RSA['ENCRYPT_KEY'])
        binance_access = rsa_decrypt.decrypt(private_key.RSA['ACCESS'])
        binance_secret = rsa_decrypt.decrypt(private_key.RSA['SECRET'])

        self.binance = ccxt.binance(config={
            'apiKey': binance_access,
            'secret': binance_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })

        self.balance = self.binance.fetch_balance(params={"type": "future"})

    def get_balance(self):
        return self.balance

    def get_binance(self):
        return self.binance

# binance = Binance()
# print(binance.get_balance())
