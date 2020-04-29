# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from .models import Stock, StockChange
import pandas
import numpy
import datetime
import redis
from api.utils import update_stock

@task()
def pull_stock_data():
    calls_per_minute = 30
    r = redis.Redis(host='localhost', port=6379, db=0)
    base = int(r.get('stock_base'))
    names = pandas.read_csv('api/namesData/stock_names.csv')

    for i in range(calls_per_minute):
        if base+i < len(names):
            print('iteration:' + str(i))
            update_stock(names['Ticker'][base+i], names['Name'][base+i])

    r.set('stock_base', base+calls_per_minute)

@task
def reset_stock_counter():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('stock_base', 0)


