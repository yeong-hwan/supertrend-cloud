import requests

def get_usd_krw():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
    exchange = requests.get(url, headers=headers).json()

    return exchange[0]['basePrice']


def get_state(state_before, state_current):
    state_now = ""

    if state_before == "cloud" and state_current == "cloud":
        state_now = "C"
    elif state_before == "upside" and state_current == "upside":
        state_now = "L"
    elif state_before == "downside" and state_current == "downside":
        state_now = "S"

    if state_before == "cloud" and state_current == "upside":
        state_now = "Crossover Out"
    elif state_before == "cloud" and state_current == "downside":
        state_now = "Crossunder Out"
    elif state_before == "upside" and state_current == "cloud":
        state_now = "Crossunder In"
    elif state_before == "downside" and state_current == "cloud":
        state_now = "Crossover In"

    if state_before == "upside" and state_current == "downside":
        state_now = "Big Short"
    elif state_before == "downside" and state_current == "upside":
        state_now = "Big Long"

    return state_now


def get_supertrend_cloud(candle, candle_type, btc=False):
    candle_close_series = candle['close']

    # current : endded[-1], before : endded[-2]
    # candle_close_current = candle_close_series[-2]
    # candle_close_before = candle_close_series[-3]

    period_1, multi_1, period_2, multi_2 = 0, 0, 0, 0
    supertrend_line_1, supertrend_line_2 = 0, 0

    long_condition, short_condition, cloud_condition = False, False, False

    # variable setting
    if candle_type == "5m":
        period_1, multi_1, period_2, multi_2 = 6, 10, 10, 6

    # elif btc == True and candle_type == "4h":
    #     period_1, multi_1, period_2, multi_2 = 4, 2.4, 4, 4.8

    # elif candle_type == "4h":
    #     period_1, multi_1, period_2, multi_2 = 10, 3, 10, 6

    # sell_state
    sell_state_current, sell_state_before = "", ""  # -2, -3

    for i in range(2, 4):
        supertrend_1 = pandas_ta.supertrend(
            high=candle['high'], low=candle['low'], close=candle['close'], period=period_1, multiplier=multi_1)
        supertrend_line_1 = supertrend_1.iloc[-i][0]

        supertrend_2 = pandas_ta.supertrend(
            high=candle['high'], low=candle['low'], close=candle['close'], period=period_2, multiplier=multi_2)
        supertrend_line_2 = supertrend_2.iloc[-i][0]

        side_at_i = get_side(candle_close_series[-i],
                              supertrend_line_1, supertrend_line_2)

        if i == 2:
            sell_state_current = side_at_i
        elif i == 3:
            sell_state_before = side_at_i

    # buy_state
    buy_state_current, buy_state_before = "", ""  # -3, -4

    for i in range(3, 5):
        supertrend_1 = pandas_ta.supertrend(
            high=candle['high'], low=candle['low'], close=candle['close'], period=period_1, multiplier=multi_1)
        supertrend_line_1 = supertrend_1.iloc[-i][0]

        supertrend_2 = pandas_ta.supertrend(
            high=candle['high'], low=candle['low'], close=candle['close'], period=period_2, multiplier=multi_2)
        supertrend_line_2 = supertrend_2.iloc[-i][0]

        side_at_i = get_side(candle_close_series[-i],
                              supertrend_line_1, supertrend_line_2)

        if i == 3:
            buy_state_current = side_at_i
        elif i == 4:
            buy_state_before = side_at_i

    sell_state = get_state(sell_state_before, sell_state_current)
    buy_state = get_state(buy_state_before, buy_state_current)

    if sell_state[-2:] == "In":
        cloud_condition = True
    elif buy_state == "Crossover Out":
        long_condition = True
    elif buy_state == "Crossunder Out":
        short_condition = True

    elif sell_state[:3] == "Big":
        cloud_condition = True
        position_side = sell_state[4:]

        if position_side == "Long":
            long_condition = True
        elif position_side == "Short":
            short_condition = True

    return long_condition, short_condition, cloud_condition, supertrend_line_1, supertrend_line_2, buy_state
