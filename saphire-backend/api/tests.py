from django.test import TestCase
from alpha_vantage.timeseries import TimeSeries
from .models import Stock, StockChange
import pandas
import numpy
import datetime
import os
import redis
from api.utils import calc_52_day_average, update_stock, calc_percent_changes

class StockUpdateTestCase(TestCase):
    key = '23V86RX6LO5AUIX4'
    ts = TimeSeries(key)

    def update_stock(self, symbol, name):
        #key = 'PLVU0FOZUJ18M46O'

        try:
            print("Symbol: " + symbol + " Name: " + name)
            stock, meta = self.ts.get_daily(symbol=symbol)
            recent_date = list(stock)[0]
            stock_dict = dict(stock[recent_date])

            stock = Stock.objects.create(name=name, date=recent_date, symbol=symbol, open=stock_dict['1. open'], high=stock_dict[
                                        '2. high'], low=stock_dict['3. low'], close=stock_dict['4. close'], vol=stock_dict['5. volume'], avg=0)
            stock.save()
            calc_52_day_average(ticker=symbol, date=recent_date)
            
        except Exception as e:
                print(e)
                
    def pull_stock_data(self):
        calls_per_minute = 30
        r = redis.Redis(host='localhost', port=6379, db=0)
        base = int(r.get('stock_base'))
        print("base: " + str(base))
        names = pandas.read_csv('api/namesData/stock_names.csv')

        for i in range(calls_per_minute):
            print("length of names list: " + str(len(names)))
            print('iteration:' + str(i))
            self.update_stock(names['Ticker'][base+i], names['Name'][base+i])

        r.set('stock_base', base+calls_per_minute)

    def reset_stock_counter(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set('stock_base', 0)
        print(r.get('stock_base'))

class CalcAverages(TestCase):

    def calc_52_day_average(self, ticker, date):
        s = Stock(date='2020-1-4', symbol='AAPL', name="Apple", vol=1, high=1, low=1, avg=2, open=1, close=1)
        s.save()
        s = Stock(date='2020-1-1', symbol='AAPL', name="Apple", vol=1, high=1, low=1, avg=2, open=1, close=4)
        s.save()
        s = Stock(date='2020-1-2', symbol='AAPL', name="Apple", vol=1, high=1, low=1, open=1, avg = 0, close=2)
        s.save()

        stock = Stock.objects.get(symbol=ticker, date=date)
        
        prev_date = date - datetime.timedelta(days=1)
        
        if Stock.objects.filter(symbol=ticker, date=prev_date).exists():
            prevStock = Stock.objects.get(symbol=ticker, date=prev_date)
            stock.avg = ((51 * prevStock.avg) + stock.close)/52
            print(stock.avg)
            stock.save()

        else:
            num_stocks = 0
            sum = 0
            for i in range(52):
                curDate = date - datetime.timedelta(days=i)
                
                if Stock.objects.filter(symbol=ticker, date=curDate).exists():
                    cur_stock = Stock.objects.get(symbol=ticker, date=curDate)
                    num_stocks += 1
                    sum += cur_stock.close

            stock.avg = sum / num_stocks
            print(stock.avg)
            stock.save()

    def calc_one_average(self):
        date = datetime.datetime.strptime('2020-1-4', '%Y-%m-%d')
        self.calc_52_day_average('AAPL', date)

class StockChangeTest(TestCase):

    def calc_percent_changes(self):
        s = Stock(date='2020-3-21', symbol='AAPL', name="Apple", vol=1, high=1, low=1, avg=2, open=1, close=1)
        s.save()
        s = Stock(date='2020-3-20', symbol='AAPL', name="Apple", vol=1, high=1, low=1, avg=2, open=1, close=1)
        s.save()
        print(datetime.date.today())
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
                print(stock_change.stock)

                stock_change.save()

class StockUpdateAndChange(TestCase):
    def execute(self):
        s = Stock(date='2020-3-22', symbol='AAPL', name="Apple", vol=1, high=1, low=1, avg=2, open=1, close=1)
        s.save()
        update_stock('AAPL', 'Apple')



        


