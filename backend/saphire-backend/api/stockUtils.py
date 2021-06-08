from .models import Stock, Company
from django.db.models import Avg, Max, Min, StdDev
from decimal import Decimal
import datetime


def get_past_days(num_days, date, ticker):
    """
    Get the past n days of stock information 
    """
    numStocks = len(Stock.objects.filter(company=ticker))
    if numStocks < num_days:
        return Stock.objects.filter(company=ticker)

    start_date = date - datetime.timedelta(days=num_days)
    stocks = Stock.objects.filter(
        company=ticker, date__range=[start_date, date])
    days = num_days

    while len(stocks) < num_days:
        start_date = date - datetime.timedelta(days=days)
        stocks = Stock.objects.filter(
            company=ticker, date__range=[start_date, date])
        days += 1
    return stocks


def fillStockFields(stock, company):
    """
    Calculate current metrics for a stock based on previous stock data for the same company.
    """
    date = stock.date
    prev_date = stock.date - datetime.timedelta(days=1)

    try:
        temp_stock_list = get_past_days(2, date, company.symbol)
        prev_stock = temp_stock_list[0]
    except Stock.DoesNotExist:
        print("dne")
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
        stock.ema_12_day = round(
            (stock.avg*Decimal(.15)) + (prev_stock.avg*Decimal(.85)), 4)
    else:
        stock.ema_12_day = round(stock.avg, 4)


def calc_ema_26_day(stock, prev_stock, company):
    if prev_stock is not None:
        stock.ema_26_day = round(
            (stock.avg*Decimal(.075)) + (prev_stock.avg*Decimal(.925)), 4)
    else:
        stock.ema_26_day = round(stock.avg, 4)


def calc_vol_ema(stock, prev_stock, company):
    if prev_stock is not None:
        stock.vol_ema = round((stock.vol*Decimal(.05)) +
                              (prev_stock.vol_ema*Decimal(.95)), 4)
    else:
        stock.vol_ema = round(stock.vol, 4)


def calc_52_day_metrics(stock, end_date, company):
    start_date = end_date - datetime.timedelta(days=52)
    stocks = Stock.objects.filter(
        company=company, date__range=[start_date, end_date])
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
        stock.stdev_52_day = 0


def calc_52_week_metrics(stock, end_date, company):
    start_date = end_date - datetime.timedelta(days=365)
    stocks = Stock.objects.filter(
        company=company, date__range=[start_date, end_date])
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
        stock.stdev_52_week = 0

    if vol_result_set['vol__avg'] is not None:
        stock.vol_avg_52_week = round(Decimal(vol_result_set['vol__avg']), 4)
    else:
        stock.vol_avg_52_week = round(stock.vol, 4)

