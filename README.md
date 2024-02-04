# Supertrend-Cloud Trading
Coin trading bot using supertrend-cloud strategy

## Strategy Overview
### What is Supertrend?
The SuperTrend indicator is a technical tool that you can use to identify trends and generate buy/sell signals. It takes the form of a single line that's overlaid onto a market's chart and follows the price action, switching from red to green as momentum shifts.

### Supertrend-Cloud
![](img/supertrend_cloud_example.jpeg?raw=true)

- We call gap between two Supertrend as **Cloud**
  - Open Long position when Crossover Cloud
  - Open Short Position When Crossunder Cloud
  - Close position when In Cloud

![](img/position_example.jpeg?raw=true)
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

### Libraries
Alert
- [Discord](https://discordpy.readthedocs.io/en/stable/)

RSA
- [RSA]()
- [cryptography]()

- - -

### Libraries
- [Discord](https://discordpy.readthedocs.io/en/stable/)
- [cryptography]()

### References
- [Supertrend-Cloud-Strategy](https://kr.tradingview.com/script/sO5mkXTE-SuperTrend-Cloud-Strategy/) by [jhanson107](https://kr.tradingview.com/u/jhanson107/)