"""High level imports for this and that"""
import json
from datetime import date
import requests

from . import config

def daily_single_stock(symbol):
    """Grab stock data"""
    function = 'TIME_SERIES_DAILY'
    url = f'{config.url}function={function}&symbol={symbol}&apikey={config.api_key}'
    print(url)
    req = requests.get(f'{url}&outputsize=compact')
    return json.loads(req.text)


def format_singles(stock_data, stock_date):
    """Formatting the output of data"""
    print(stock_data)
    symbol = stock_data['Meta Data']['2. Symbol']
    daily = stock_data['Time Series (Daily)']
    stock_open = '{:.2f}'.format(float(daily[stock_date]['1. open']))
    stock_high = '{:.2f}'.format(float(daily[stock_date]['2. high']))
    stock_low = '{:.2f}'.format(float(daily[stock_date]['3. low']))
    stock_close = '{:.2f}'.format(float(daily[stock_date]['4. close']))
    output = f'{symbol} opened at ${stock_open} and closed at ${stock_close} with a high of \
${stock_high} and a low of ${stock_low} on {stock_date}'
    return output


def many_stocks(symbols):
    """Grab multiple stock data"""
    function = 'BATCH_STOCK_QUOTES'
    url = f'{config.url}function={function}&symbol={symbols}&apikey={config.api_key}'
    req = requests.get(url)
    req_json = json.loads(req.text)
    return req_json['Stock Quotes']
