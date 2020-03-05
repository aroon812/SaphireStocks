from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    watchedStocks = models.ManyToManyField('Stock', blank=True, related_name='watchedBy')
    
class Stock(models.Model):
    #watchedBy = models.ManyToManyField('User', blank=True, related_name='watchedStocks')
    date = models.DateField()
    symbol = models.CharField(max_length=5, default='', blank=True, null=True)
    name = models.CharField(max_length=200, default='', blank=True, null=True)
    vol = models.IntegerField()
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    avg = models.DecimalField(max_digits=10, decimal_places=4)
    open = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return str(self.name)

class StockChange(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    date = models.DateField()
    vol = models.IntegerField()
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    avg = models.DecimalField(max_digits=10, decimal_places=4)
    open = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return str(self.stock.name)