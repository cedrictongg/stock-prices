"""High level imports for this and that"""
import json
import requests

from . import config


def daily_intraday_stock(symbol):
    """Grabs the latest data"""
    function = 'TIME_SERIES_INTRADAY'
    url = f'{config.url}function={function}&symbol={symbol}&interval=1min&outputsize=compact'
    req = requests.get(f'{url}&apikey={config.api_key}')
    print(url)
    return json.loads(req.text)


def open_format_intraday(stock_data):
    """Formatting the output of open data"""
    if 'Meta Data' in stock_data:
        symbol = stock_data['Meta Data']['2. Symbol']
        daily = stock_data['Time Series (1min)']
        date = list(stock_data['Time Series (1min)'].keys())[0]
        stock_open = '{:.2f}'.format(float(daily[date]['1. open']))
        stock_high = '{:.2f}'.format(float(daily[date]['2. high']))
        stock_low = '{:.2f}'.format(float(daily[date]['3. low']))
        output = f'{symbol} is currently at ${stock_open} with a high of \
${stock_high} and a low of ${stock_low} today.'
        return output
    return 'I could not find any stock information about that company.'


def daily_single_stock(symbol):
    """Grab stock data"""
    function = 'TIME_SERIES_DAILY'
    url = f'{config.url}function={function}&symbol={symbol}&outputsize=compact'
    req = requests.get(f'{url}&apikey={config.api_key}')
    print(url)
    return json.loads(req.text)


def closed_format_singles(stock_data, stock_date):
    """Formatting the output of closed data"""
    print(stock_data)
    if 'Meta Data' in stock_data:
        symbol = stock_data['Meta Data']['2. Symbol']
        daily = stock_data['Time Series (Daily)']
        stock_open = '{:.2f}'.format(float(daily[stock_date]['1. open']))
        stock_high = '{:.2f}'.format(float(daily[stock_date]['2. high']))
        stock_low = '{:.2f}'.format(float(daily[stock_date]['3. low']))
        stock_close = '{:.2f}'.format(float(daily[stock_date]['4. close']))
        output = f'{symbol} opened at ${stock_open} and closed at ${stock_close} with a high of \
${stock_high} and a low of ${stock_low} as of {stock_date}.'
        return output
    return 'I could not find any stock information about that company.'


def many_stocks(symbols):
    """Grab multiple stock data"""
    function = 'BATCH_STOCK_QUOTES'
    url = f'{config.url}function={function}&symbol={symbols}&apikey={config.api_key}'
    req = requests.get(url)
    req_json = json.loads(req.text)
    return req_json['Stock Quotes']
