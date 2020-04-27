from .models import Stock, StockChange, Company
from django.db.models import Avg, Max, Min, StdDev
from decimal import Decimal
import datetime

def fillStockFields(stock, company):
    date = stock.date
    prev_date = stock.date - datetime.timedelta(days=1)
    
    try:
        prev_stock = Stock.objects.get(company=company, date=prev_date)
    except Stock.DoesNotExist:
        prev_stock = None
    
    calc_range(stock)
    calc_avg(stock)
    calc_single_day_change(stock)
    calc_day_to_day_change(stock, prev_stock, company)
    calc_ema_12_day(stock, prev_stock, company)
    calc_ema_26_day(stock, prev_stock, company)
    calc_vol_ema(stock, prev_stock, company)
    calc_52_day_metrics(stock, date, company)
    calc_52_week_metrics(stock, date, company)
    """
    print("vol: " + str(stock.vol) + " type: " + str(type(stock.vol)))
    print("high: " + str(stock.high) + " type: " + str(type(stock.high)))
    print("low: " + str(stock.low) + " type: " + str(type(stock.low)))
    print("open: " + str(stock.open) + " type: " + str(type(stock.open)))
    print("close: " + str(stock.close) + " type: " + str(type(stock.close)))
    print("avg: " + str(stock.avg) + " type: " + str(type(stock.avg)))
    print("range: " + str(stock.range) + " type: " + str(type(stock.range)))
    print("single_day_change: " + str(stock.single_day_change) + " type: " + str(type(stock.single_day_change)))
    print("day_to_day_change: " + str(stock.day_to_day_change) + " type: " + str(type(stock.day_to_day_change)))
    print("ema_12_day: " + str(stock.ema_12_day) + " type: " + str(type(stock.ema_12_day)))
    print("ema_26_day: " + str(stock.ema_26_day) + " type: " + str(type(stock.ema_26_day)))
    print("vol_ema: " + str(stock.vol_ema) + " type: " + str(type(stock.vol_ema)))
    print("vol_avg_52_week: " + str(stock.vol_avg_52_week) + " type: " + str(type(stock.vol_avg_52_week)))
    print("high_52_day: " + str(stock.high_52_day) + " type: " + str(type(stock.high_52_day)))
    print("high_52_week: " + str(stock.high_52_week) + " type: " + str(type(stock.high_52_week)))
    print("low_52_day: " + str(stock.low_52_day) + " type: " + str(type(stock.low_52_day)))
    print("low_52_week: " + str(stock.low_52_week) + " type: " + str(type(stock.low_52_week)))
    print("avg_52_day: " + str(stock.avg_52_day) + " type: " + str(type(stock.avg_52_day)))
    print("avg_52_week: " + str(stock.avg_52_week) + " type: " + str(type(stock.avg_52_week)))
    print("stdev_52_day: " + str(stock.stdev_52_day) + " type: " + str(type(stock.stdev_52_day)))
    print("stdev_52_week: " + str(stock.stdev_52_week) + " type: " + str(type(stock.stdev_52_week)))
    """
    stock.save()

def calc_range(stock):
    stock.range = round(stock.high - stock.low, 4)

def calc_avg(stock):
    stock.avg = round((stock.high + stock.low + stock.close)/3, 4)

def calc_single_day_change(stock):
    stock.single_day_change = round(stock.close - stock.open, 4)

def calc_day_to_day_change(stock, prev_stock, company):
    if prev_stock is not None:
        stock.day_to_day_change = round(stock.close - prev_stock.close, 4)
    else:
        stock.day_to_day_change = round(stock.close, 4)

def calc_ema_12_day(stock, prev_stock, company):
    if prev_stock is not None:
        stock.ema_12_day = round((stock.avg*Decimal(.15)) + (prev_stock.avg*Decimal(.85)), 4)
    else:
        stock.ema_12_day = round(stock.avg, 4)

def calc_ema_26_day(stock, prev_stock, company):
    if prev_stock is not None:
        stock.ema_26_day = round((stock.avg*Decimal(.075)) + (prev_stock.avg*Decimal(.925)), 4)
    else:
        stock.ema_26_day = round(stock.avg, 4)

def calc_vol_ema(stock, prev_stock, company):
    if prev_stock is not None:
        stock.vol_ema = round((stock.vol*Decimal(.05)) + (prev_stock.vol_ema*Decimal(.95)), 4)
    else:
        stock.vol_ema = round(stock.vol, 4)

def calc_52_day_metrics(stock, end_date, company):
    start_date = end_date - datetime.timedelta(days=52)
    stocks = Stock.objects.filter(company=company, date__range=[start_date, end_date])
    high_result_set = stocks.aggregate(Max('high'))
    low_result_set = stocks.aggregate(Min('low'))
    avg_result_set = stocks.aggregate(Avg('close'))
    stdev_result_set = stocks.aggregate(StdDev('close'))
    if high_result_set['high__max'] is not None:
        stock.high_52_day = round(high_result_set['high__max'], 4)   
    else:
        stock.high_52_day = round(stock.high, 4)

    if low_result_set['low__min'] is not None:
            stock.low_52_day = round(low_result_set['low__min'], 4)
    else:
        stock.low_52_day = round(stock.low, 4)

    if avg_result_set['close__avg'] is not None:
        stock.avg_52_day = round(avg_result_set['close__avg'], 4)
    else:
        stock.avg_52_day = round(stock.close, 4)

    if stdev_result_set['close__stddev'] is not None:
        stock.stdev_52_day = round(stdev_result_set['close__stddev'], 4)
    else:
        stock.stdev_52_day = round(stock.close, 4)

def calc_52_week_metrics(stock, end_date, company):
    start_date = end_date - datetime.timedelta(days=365)
    stocks = Stock.objects.filter(company=company, date__range=[start_date, end_date])
    
    high_result_set = stocks.aggregate(Max('high'))
    low_result_set = stocks.aggregate(Min('low'))
    avg_result_set = stocks.aggregate(Avg('close'))
    stdev_result_set = stocks.aggregate(StdDev('close'))
    vol_result_set = stocks.aggregate(Avg('vol'))

    if high_result_set['high__max'] is not None:
        stock.high_52_week = round(high_result_set['high__max'], 4)  
    else:
        stock.high_52_week = round(stock.high, 4)

    if low_result_set['low__min'] is not None:
        stock.low_52_week = round(low_result_set['low__min'], 4)
    else:
        stock.low_52_week = round(stock.low, 4)

    if avg_result_set['close__avg'] is not None:
        stock.avg_52_week = round(avg_result_set['close__avg'], 4)
    else:
        stock.avg_52_week = round(stock.close, 4)

    if stdev_result_set['close__stddev'] is not None:
        stock.stdev_52_week = round(stdev_result_set['close__stddev'], 4)
    else:
        stock.stdev_52_week = round(stock.close, 4)

    if vol_result_set['vol__avg'] is not None:
        stock.vol_avg_52_week = round(Decimal(vol_result_set['vol__avg']), 4)
    else:
        stock.vol_avg_52_week = round(stock.vol, 4)

