# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from alpha_vantage.timeseries import TimeSeries
from .models import Stock, StockChange
import pandas
import numpy
import datetime

key = '23V86RX6LO5AUIX4'
ts = TimeSeries(key)

def updateStock(self, symbol, name):
        #key = 'PLVU0FOZUJ18M46O'

        try:
            print("symbol " + str(symbol))
            stock, meta = ts.get_daily(symbol=symbol)
            recentDate = list(stock)[0]
            stockDict = dict(stock[recentDate])

            stock = Stock.objects.create(date=recentDate, symbol=symbol, open=stockDict['1. open'], high=stockDict[
                                        '2. high'], low=stockDict['3. low'], close=stockDict['4. close'], vol=stockDict['5. volume'], avg=0, name=name)
            stock.save()
            
        except Exception as e:
                print(e)

@task()       
def pullStockData(self):
    now = datetime.datetime.now()
    print("hour " + str(now.hour))
        
    base = now.hour * 60
    names = pandas.read_csv('api/namesData/stock_names.csv')

    for i in range(30):
        print('iteration:' + str(i))
        updateStock(names['Ticker'][base+i], names['Name'][base+i])

@task()
def calcPercentChanges():
    print("temp")


    
        
