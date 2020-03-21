# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from alpha_vantage.timeseries import TimeSeries
from .models import Stock, StockChange
import pandas
import numpy
import datetime
import redis

key = '23V86RX6LO5AUIX4'
ts = TimeSeries(key)

def update_stock(self, symbol, name):
        #key = 'PLVU0FOZUJ18M46O'

        try:
            print("symbol " + str(symbol))
            stock, meta = ts.get_daily(symbol=symbol)
            recent_date = list(stock)[0]
            stock_dict = dict(stock[recent_date])

            stock = Stock.objects.create(date=recent_date, symbol=symbol, open=stock_dict['1. open'], high=stock_dict[
                                        '2. high'], low=stock_dict['3. low'], close=stock_dict['4. close'], vol=stock_dict['5. volume'], avg=0, name=name)
            stock.save()
            
        except Exception as e:
                print(e)

@task()       
def pull_stock_data(self):
    calls_per_minute = 30
    r = redis.Redis(host='localhost', port=6379, db=0)
    base = int(r.get('stock_base'))
    names = pandas.read_csv('api/namesData/stock_names.csv')

    for i in range(calls_per_minute):
        if base+i < len(names):
            print('iteration:' + str(i))
            update_stock(names['Ticker'][base+i], names['Name'][base+i])

    r.set('stock_base', base+calls_per_minute)

@task()
def reset_stock_counter():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('stock_base', 0)

@task()
def calc_percent_changes():
    print("temp")