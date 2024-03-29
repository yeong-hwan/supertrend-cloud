# Supertrend-Cloud Trading
Coin trading bot using supertrend-cloud strategy

## Strategy Overview
### What is Supertrend?
The SuperTrend indicator is a technical tool that you can use to identify trends and generate buy/sell signals. It takes the form of a single line that's overlaid onto a market's chart and follows the price action, switching from red to green as momentum shifts.

<p align="center">
  <img src="img/supertrend.png" alt="drawing" width="600"/>
</p>

### Supertrend-Cloud
<img src="img/supertrend_cloud_example.jpeg" alt="drawing" width="800"/>

- We call gap between two Supertrend as Cloud
  - Crossover Cloud: Open Long position
  - Crossunder Cloud: Open Short position
  - In Cloud: Close position

<img src="img/position_example.jpeg" alt="drawing" width="800"/>

- In a big short or big long situation, it closes the position and opens the opposite position at the same time

- - -

## Setting
### Supertrend Parameter

### private-key
Server
- ASW EC2 pem key  

Alert
- Discord Channel ID
- Discord Bot Token

RSA
- Encrypt Key
- ACCESS(RSA Encryption using Binance API Key)
- SECRET(RSA Encryption using Binance Secret Key)

- - -

## Libraries
### conda
Alert
  - [Discord](https://discordpy.readthedocs.io/en/stable/)

RSA
  - [RSA](https://pypi.org/project/rsa/)
  - [cryptography](https://pypi.org/project/cryptography/)


### pip(by conda)
CCXT(Binance)
  - [CCXT(version 2.5.67)](https://github.com/ccxt/ccxt)

Math
  - [numpy](https://numpy.org/)
  - [Pandas](https://pandas.pydata.org/)
  - [Pandas TA](https://github.com/twopirllc/pandas-ta)

## References
- [Supertrend-Cloud-Strategy](https://kr.tradingview.com/script/sO5mkXTE-SuperTrend-Cloud-Strategy/) by [jhanson107](https://kr.tradingview.com/u/jhanson107/)