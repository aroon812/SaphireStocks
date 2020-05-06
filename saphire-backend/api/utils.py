from __future__ import absolute_import, unicode_literals
from celery import task
from alpha_vantage.timeseries import TimeSeries
from .models import Stock, StockChange, Company
from .serializers import StockSerializer
import pandas
import numpy
from datetime import datetime, timedelta
import redis

key = '23V86RX6LO5AUIX4'
ts = TimeSeries(key)

def update_historical_stocks():
    names = pandas.read_csv('api/namesData/stock_names.csv')
    with open('/home/stockteam/saphire/saphire-backend/api/update_file.txt', 'r') as progress_file:
            tickers_list = progress_file.read().splitlines()
            progress_file.close()

    for i in range(len(names)):
        if names['Ticker'][i] not in tickers_list:
            print('current company:' + names['Ticker'][i])
            create_company(names['Ticker'][i], names['Name'][i])
            update_historical_stock_single(names['Ticker'][i])

            with open('/home/stockteam/saphire/saphire-backend/api/update_file.txt', 'w') as progress_file:
                tickers_list.append(names['Ticker'][i])
                for ticker in tickers_list:
                    progress_file.write('%s\n' % ticker)
                progress_file.close()
            

def update_historical_stock_single(symbol):
    try: 
        stock, meta = ts.get_daily(symbol=symbol, outputsize='full')
        company = Company.objects.get(symbol=symbol)
        dates = list(stock)
        dates.reverse()
        today = datetime.strptime(str(datetime.date(datetime.today())), '%Y-%m-%d')
        cutoff = today - timedelta(days=1825)

        for date in dates:
            if datetime.strptime(date, '%Y-%m-%d') >= cutoff:
                #print(symbol + " " + str(len(dates)) + " " + str(date))
                stock_dict = dict(stock[date]) 
                
                validated_data = {
                    'date': date,
                    'company': symbol,
                    'open': stock_dict['1. open'], 
                    'high': stock_dict['2. high'], 
                    'low': stock_dict['3. low'], 
                    'close': stock_dict['4. close'], 
                    'vol':stock_dict['5. volume']
                }
                
                serializer = StockSerializer(data=validated_data)
                if serializer.is_valid():
                    serializer.save()
                    
    except Exception as e:
        print(e)

def create_company(symbol, name):
    if not Company.objects.filter(symbol=symbol, name=name).exists():
        print(symbol)
        print(name)
        company = Company.objects.create(symbol=symbol, name=name)
        company.save()


def update_stock(symbol, name):

        try:
            create_company(symbol, name)
            stock, meta = ts.get_daily(symbol=symbol)
            print(stock)
            recent_date = list(stock)[0]
            stock_dict = dict(stock[recent_date])
            validated_data = {
                    'date': recent_date,
                    'company': symbol,
                    'open': stock_dict['1. open'], 
                    'high': stock_dict['2. high'], 
                    'low': stock_dict['3. low'], 
                    'close': stock_dict['4. close'], 
                    'vol':stock_dict['5. volume']
                }
                
            serializer = StockSerializer(data=validated_data)
            if serializer.is_valid():
                serializer.save()
                    
            """
            company = Company.objects.get(symbol=symbol)
            stock = Stock.objects.create(company=company, date=recent_date, open=stock_dict['1. open'], high=stock_dict[
                                        '2. high'], low=stock_dict['3. low'], close=stock_dict['4. close'], vol=stock_dict['5. volume'], avg=0)
            stock.save()
            calc_52_day_average(symbol=symbol, date=recent_date)
            calc_percent_changes(symbol=symbol, date=recent_date)
            """
            
        except Exception as e:
                print(e)



