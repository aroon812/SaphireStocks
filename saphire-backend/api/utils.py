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

def update_stock(symbol, name):

        try:
            stock, meta = ts.get_daily(symbol=symbol)
            print(stock)
            recent_date = list(stock)[0]
            stock_dict = dict(stock[recent_date])

            stock = Stock.objects.create(date=recent_date, symbol=symbol, open=stock_dict['1. open'], high=stock_dict[
                                        '2. high'], low=stock_dict['3. low'], close=stock_dict['4. close'], vol=stock_dict['5. volume'], avg=0, name=name)
            stock.save()
            calc_52_day_average(symbol=symbol, date=recent_date)
            calc_percent_changes(symbol=symbol, date=recent_date)
            
        except Exception as e:
                print(e)

def calc_52_day_average(symbol, date):
        print(date)
        stock = Stock.objects.get(symbol=symbol, date=date)
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        prev_date = date - datetime.timedelta(days=1)
        
        if Stock.objects.filter(symbol=symbol, date=prev_date).exists():
            prevStock = Stock.objects.get(symbol=symbol, date=prev_date)
            stock.avg = ((51 * prevStock.avg) + stock.close)/52
            print('prev exists')
            print(stock.avg)
            stock.save()

        else:
            num_stocks = 0
            sum = 0
            for i in range(52):
                curDate = date - datetime.timedelta(days=i)
                
                if Stock.objects.filter(symbol=symbol, date=curDate).exists():
                    cur_stock = Stock.objects.get(symbol=symbol, date=curDate)
                    num_stocks += 1
                    sum += cur_stock.close

            stock.avg = sum / num_stocks
            print('prev does not exist')
            print(stock.avg)
            stock.save()

def calc_percent_changes(symbol, date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    before = date - datetime.timedelta(days=1)
    stock = Stock.objects.get(symbol=symbol, date=date)

    if Stock.objects.filter(symbol=stock.symbol, date=before).exists():
        prev_stock = Stock.objects.get(symbol=stock.symbol, date=before)
        vol = (stock.vol - prev_stock.vol)/prev_stock.vol
        high = (stock.high - prev_stock.avg)/prev_stock.avg
        low = (stock.low - prev_stock.avg)/prev_stock.avg
        avg = (stock.avg - prev_stock.avg)/prev_stock.avg
        open = (stock.open - prev_stock.avg)/prev_stock.avg
        close = (stock.close - prev_stock.avg)/prev_stock.avg
        stock_change = StockChange(stock=stock, date=stock.date, vol=vol, high=high, low=low, avg=avg, open=open, close=close)

        stock_change.save()

