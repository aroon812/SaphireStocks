# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from alpha_vantage.timeseries import TimeSeries

key = 'PLVU0FOZUJ18M46O'
ts = TimeSeries(key)
aapl, meta = ts.get_daily(symbol='AAPL')

@task()
def task1():
    print(aapl)
    


