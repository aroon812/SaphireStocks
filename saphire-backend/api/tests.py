from django.test import TestCase
from alpha_vantage.timeseries import TimeSeries
from .models import Stock, StockChange
import pandas
import numpy
import datetime
import os



class StockUpdateTestCase(TestCase):
    key = '23V86RX6LO5AUIX4'
    ts = TimeSeries(key)

    def updateStock(self, symbol, name):
        #key = 'PLVU0FOZUJ18M46O'

        try:
            print("Symbol: " + symbol + " Name: " + name)
            stock, meta = self.ts.get_daily(symbol=symbol)
            recentDate = list(stock)[0]
            stockDict = dict(stock[recentDate])

            stock = Stock.objects.create(name=name, date=recentDate, symbol=symbol, open=stockDict['1. open'], high=stockDict[
                                        '2. high'], low=stockDict['3. low'], close=stockDict['4. close'], vol=stockDict['5. volume'], avg=0)
            stock.save()
            
        except Exception as e:
                print(e)
                
    def pullStockData(self):
        now = datetime.datetime.now()
        print("hour " + str(now.hour))
          
        base = now.hour * 60
        names = pandas.read_csv('api/namesData/stock_names.csv')
     
        for i in range(30):
            print('iteration:' + str(i))
            print(type(names['Ticker'][0]))
            self.updateStock(names['Ticker'][base+i], names['Name'][base+i])

class CalcAverages(TestCase):

    def calc52DayAverage(self, ticker, date):
        s = Stock(date='2020-1-4', symbol='AAPL', name="Apple", vol=1, high=1, low=1, avg=2, open=1, close=1)
        s.save()
        s = Stock(date='2020-1-1', symbol='AAPL', name="Apple", vol=1, high=1, low=1, avg=2, open=1, close=1)
        s.save()
        s = Stock(date='2020-1-2', symbol='AAPL', name="Apple", vol=1, high=1, low=1, open=1, avg = 0, close=1)
        s.save()

        stock = Stock.objects.get(symbol=ticker, date=date)
        
        prevDate = date - datetime.timedelta(days=1)
        
        if Stock.objects.filter(symbol=ticker, date=prevDate).exists():
            prevStock = Stock.objects.get(symbol=ticker, date=prevDate)
            stock.avg = ((51 * prevStock.avg) + stock.close)/52
            print(stock.avg)
            stock.save()

        else:
            prices = []
            sum = 0
            for i in range(52):
                curDate = date - datetime.timedelta(days=i)
                
                if Stock.objects.filter(symbol=ticker, date=curDate).exists():
                    curStock = Stock.objects.get(symbol=ticker, date=curDate)
                    prices.append(curStock.close)
                    sum += curStock.close

            stock.avg = sum / len(prices)
            print(stock.avg)
            stock.save()

    def calcOneAverage(self):
        date = datetime.datetime.strptime('2020-1-4', '%Y-%m-%d')
        self.calc52DayAverage('AAPL', date)



        


