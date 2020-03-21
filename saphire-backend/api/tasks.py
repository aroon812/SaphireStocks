# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from alpha_vantage.timeseries import TimeSeries
from .models import Stock, StockChange
import pandas
import numpy
import datetime
import redis
import datetime
from api.utils import calc_52_day_average

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
            calc_52_day_average(ticker=symbol, date=recent_date)
            
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
def calc_percent_changes(self):

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    today = datetime.date.today()
    stocks = Stock.objects.filter(date=today)

    for stock in stocks:
        if Stock.objects.filter(symbol=stock.symbol, date=yesterday).exists():
            prev_stock = Stock.objects.get(symbol=stock.symbol, date=yesterday)
            vol = (stock.vol - prev_stock.vol)/prev_stock.vol
            high = (stock.high - prev_stock.avg)/prev_stock.avg
            low = (stock.low - prev_stock.avg)/prev_stock.avg
            avg = (stock.avg - prev_stock.avg)/prev_stock.avg
            open = (stock.open - prev_stock.avg)/prev_stock.avg
            close = (stock.close - prev_stock.avg)/prev_stock.avg
            stock_change = StockChange(stock=stock, date=stock.date, vol=vol, high=high, low=low, avg=avg, open=open, close=close)

            stock_change.save()
