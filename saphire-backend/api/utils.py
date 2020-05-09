from __future__ import absolute_import, unicode_literals
from celery import task
from alpha_vantage.timeseries import TimeSeries
from .models import Stock, StockChange, Company
from .serializers import StockSerializer
from django.db.models import Max, Min
import statistics
import pandas
import numpy
from datetime import datetime, timedelta
from .stockUtils import get_past_days
import redis

key = '23V86RX6LO5AUIX4'
ts = TimeSeries(key)



def current_day_info(ticker):
    stock, meta = ts.get_intraday(symbol=ticker, interval='1min')
    recent = list(stock)[0]
    stocks = Stock.objects.filter(company=ticker)
    
    recent_date = stocks.aggregate(Max('date'))
    date_str = recent_date['date__max']
    prev_stock = Stock.objects.get(company=ticker, date=date_str)
    print(prev_stock.low_52_week)
    
    high = float(stock[recent]['2. high'])
    low = float(stock[recent]['3. low'])
    close = float(stock[recent]['4. close'])
    volume = float(stock[recent]['5. volume'])
    percent_change = ((float(stock[recent]['4. close']) - float(prev_stock.close))/float(prev_stock.close)) * 100
    day_range = float(stock[recent]['2. high']) - float(stock[recent]['3. low'])
    
    if high > float(prev_stock.high_52_day):
        high_52_day = high
    else:
        high_52_day = float(prev_stock.high_52_day)
    if low < float(prev_stock.high_52_day):
        low_52_day = low
    else:
        low_52_day = float(prev_stock.low_52_day)
    
    avg = (high + low + close)/3
    range_52_day = high_52_day - low_52_day
    ema_12_day = (avg*.15) + (float(prev_stock.avg)*.85)
    ema_26_day = (avg*.075) + (float(prev_stock.avg)*.925)
    start_date = date_str - timedelta(days=20)
    #last_20_days = Stock.objects.filter(company=ticker, date__range=[start_date, date_str])
    last_20_days = get_past_days(20, date_str, ticker)
    closes = []
    for day in last_20_days:
        closes.append(float(day.close))
    closes.append(close)
    print(len(closes))
    stdev_20_day = statistics.stdev(closes)

    oscillator_stocks = get_past_days(14, date_str, ticker)
    high_result_set = oscillator_stocks.aggregate(Max('high'))
    low_result_set = oscillator_stocks.aggregate(Min('low'))
    high_14_day = float(high_result_set['high__max'])
    low_14_day = float(low_result_set['low__min'])
    difference = high_14_day - low_14_day
    if difference == 0:
        stochastic_oscillator = 0
    else:
        stochastic_oscillator = ((close - low_14_day)/(high_14_day - low_14_day))*100
    
    recent_data = {
        'current_price' : close,
        'previous_close': float(prev_stock.close),
        'open': float(stock[recent]['1. open']),
        'percent_change': percent_change,
        'range': day_range,
        '52_day_range': range_52_day,
        '52_day_high': high_52_day,
        '52_day_low': low_52_day,
        'vol': int(stock[recent]['5. volume']),
        '12_day_ema': ema_12_day,
        '26_day_ema': ema_26_day,
        '20_day_stdev': stdev_20_day,
        'stochastic_oscillator': stochastic_oscillator
    }
    
    return recent_data

def update_historical_stocks():
    names = pandas.read_csv('api/namesData/100_names_data.csv')
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
    if not Company.objects.filter(symbol=symbol).exists():
        print(symbol)
        print(name)
        company = Company.objects.create(symbol=symbol, name=name)
        company.save()


def update_stock(symbol, name):

        try:
            create_company(symbol, name)
            stock, meta = ts.get_daily(symbol=symbol)
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
            
        except Exception as e:
                print(e)



