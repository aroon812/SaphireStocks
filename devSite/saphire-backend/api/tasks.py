# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task

@task()
def task1():
    print("Bigtuba")


