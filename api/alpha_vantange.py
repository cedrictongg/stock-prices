"""High level imports for this and that"""
import json
from datetime import date
import requests
import config

def daily_single_stock(function, symbol):
    """Grab stock data"""
    url = f'{config.url}function={function}&symbol={symbol}&apikey={config.api_key}'
    req = requests.get(f'{url}&outputsize=compact')
    req_json = json.loads(req.text)
    return req_json['Time Series (Daily)']


def format_singles(stock_data, stock_date):
    """Formatting the output of data"""
    stock_open = '{:.2f}'.format(float(stock_data[stock_date]['1. open']))
    stock_high = '{:.2f}'.format(float(stock_data[stock_date]['2. high']))
    stock_low = '{:.2f}'.format(float(stock_data[stock_date]['3. low']))
    stock_close = '{:.2f}'.format(float(stock_data[stock_date]['4. close']))
    output = f'Opened at {stock_open} and closed at {stock_close} with a high of {stock_high} \
and a low of {stock_low}'
    return output


def many_stocks(symbols):
    """Grab multiple stock data"""
    function = 'BATCH_STOCK_QUOTES'
    url = f'{config.url}function={function}&symbol={symbols}&apikey={config.api_key}'
    req = requests.get(url)
    req_json = json.loads(req.text)
    return req_json['Stock Quotes']


date_input = date.strftime(date.today(), '%Y-%m-%d')
# singles_data = daily_single_stock('TIME_SERIES_DAILY', 'MSFT')
# stock_output = format_singles(singles_data, date_input)
# print(stock_output)
