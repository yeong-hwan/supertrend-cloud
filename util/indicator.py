import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from constants import constants

import requests
import pandas_ta


def get_usd_krw():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
    exchange = requests.get(url, headers=headers).json()

    return exchange[0]['basePrice']


def get_side(candle_close_current, st_1, st_2):
    result = ""

    SIDE = constants.SIDE

    if ((candle_close_current < st_1) & (candle_close_current > st_2)) \
    or ((candle_close_current > st_1) & (candle_close_current < st_2)):
        result = SIDE['CLOUD']

    if (candle_close_current > st_1) & (candle_close_current > st_2):
        result = SIDE['ABOVE']

    if (candle_close_current < st_1) & (candle_close_current < st_2):
        result = SIDE['BELOW']

    return result


def get_state(sides):
    side_before, side_current = sides
    state_now = ""

    CLOUD = constants.SIDE['CLOUD']
    ABOVE = constants.SIDE['ABOVE']
    BELOW = constants.SIDE['BELOW']
    STATE = constants.STATE

    if side_before == CLOUD and side_current == CLOUD:
        state_now = STATE['STABLE']['CLOUD']
    elif side_before == ABOVE and side_current == ABOVE:
        state_now = STATE['STABLE']['ABOVE']
    elif side_before == BELOW and side_current == BELOW:
        state_now = STATE['STABLE']['BELOW']

    if side_before == CLOUD and side_current == ABOVE:
        state_now = STATE['CROSS']['OVER']['OUT']
    elif side_before == CLOUD and side_current == BELOW:
        state_now = STATE['CROSS']['UNDER']['OUT']
    elif side_before == ABOVE and side_current == CLOUD:
        state_now = STATE['CROSS']['UNDER']['IN']
    elif side_before == BELOW and side_current == CLOUD:
        state_now = STATE['CROSS']['OVER']['IN']

    if side_before == ABOVE and side_current == BELOW:
        state_now = STATE['BIG']['SHORT']
    elif side_before == BELOW and side_current == ABOVE:
        state_now = STATE['BIG']['LONG']

    return state_now

def get_supertrend(candle, period, multiplier):
    supertrend = pandas_ta.supertrend(
        high = candle['high'],
        low = candle['low'],
        close = candle['close'],
        period = period,
        multiplier = multiplier
    )

    return supertrend

def get_supertrend_line(supertrend, idx):
    return supertrend.iloc[-idx].iloc[0]

def get_supertrend_lines(candle, settings, idx):
    supertrend_line_1, supertrend_line_2 = 0, 0
    PERIOD_1, MULTIPLIER_1, PERIOD_2, MULTIPLIER_2 = settings

    supertrend_1 = get_supertrend(candle, PERIOD_1, MULTIPLIER_1)
    supertrend_line_1 = get_supertrend_line(supertrend_1, idx)

    supertrend_2 = get_supertrend(candle, PERIOD_2, MULTIPLIER_2)
    supertrend_line_2 = get_supertrend_line(supertrend_2, idx)

    return (supertrend_line_1, supertrend_line_2)


def get_sell_sides(candle, settings):
    close_of_candles = candle['close']

    # sell_state
    sell_side_current, sell_side_before = "", ""  # -2, -3

    for idx in range(2, 4):
        supertrend_line_1, supertrend_line_2 = get_supertrend_lines(candle, settings, idx)

        sell_side = get_side(close_of_candles.iloc[-idx],
                            supertrend_line_1, supertrend_line_2)

        if idx == 2:
            sell_side_current = sell_side
        elif idx == 3:
            sell_side_before = sell_side

    return (sell_side_before, sell_side_current)

def get_buy_sides(candle, settings):
    close_of_candles = candle['close']

    # buy_state
    buy_side_current, buy_side_before = "", ""  # -3, -4

    for idx in range(3, 5):
        supertrend_line_1, supertrend_line_2 = get_supertrend_lines(candle, settings, idx)

        buy_side = get_side(close_of_candles.iloc[-idx],
                            supertrend_line_1, supertrend_line_2)

        if idx == 3:
            buy_side_current = buy_side
        elif idx == 4:
            buy_side_before = buy_side
        
    return (buy_side_before, buy_side_current)

def get_supertrend_cloud(candle, candle_type="5m", btc=False):
    PERIOD_1, MULTIPLIER_1, PERIOD_2, MULTIPLIER_2 = 0, 0, 0, 0
    supertrend_line_1, supertrend_line_2 = 0, 0

    long_condition, short_condition, cloud_condition = False, False, False

    # variable setting
    SUPERTREND = constants.SUPERTREND

    if candle_type == "5m":
        PERIOD_1 = SUPERTREND['5M']['PERIOD_1']
        MULTIPLIER_1 = SUPERTREND['5M']['MULTIPLIER_1']
        PERIOD_2 = SUPERTREND['5M']['PERIOD_2']
        MULTIPLIER_2 = SUPERTREND['5M']['MULTIPLIER_2']

    # elif btc == True and candle_type == "4h":
    #     period_1, multi_1, period_2, multi_2 = 4, 2.4, 4, 4.8

    # elif candle_type == "4h":
    #     period_1, multi_1, period_2, multi_2 = 10, 3, 10, 6
    settings = (PERIOD_1, MULTIPLIER_1, PERIOD_2, MULTIPLIER_2)

    sell_sides = get_sell_sides(candle, settings)
    buy_sides = get_buy_sides(candle, settings)

    sell_state = get_state(sell_sides)
    buy_state = get_state(buy_sides)

    orders = check_order(sell_state, buy_state)

    return orders
    # return long_condition, short_condition, cloud_condition, supertrend_line_1, supertrend_line_2, buy_state

def check_order(sell_state, buy_state):
    POSITION = constants.POSITION
    open_long, open_short, close_position = (False, False, False)

    if sell_state in POSITION['CLOSE']:
        close_position = True
    if buy_state in POSITION['OPEN']['LONG']:
        open_long = True
    if buy_state in POSITION['OPEN']['SHORT']:
        open_long = True

    return (open_long, open_short, close_position)
