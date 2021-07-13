from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Company(models.Model):
    """
    A company object. Just a symbol and a name for each entry in the database.
    """
    symbol = models.CharField(
        max_length=5, default='', blank=True, null=False, unique=True, primary_key=True)
    name = models.CharField(max_length=200, default='', blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Stock(models.Model):
    """
    A single day for the stocks of a company.
    """
    date = models.DateField(null=False)
    company = models.ForeignKey(
        'Company', on_delete=models.CASCADE, null=False)
    vol = models.IntegerField(null=False)
    high = models.DecimalField(max_digits=15, decimal_places=4, null=False)
    low = models.DecimalField(max_digits=15, decimal_places=4, null=False)
    open = models.DecimalField(max_digits=15, decimal_places=4, null=False)
    close = models.DecimalField(max_digits=15, decimal_places=4, null=False)
    avg = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    range = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    single_day_change = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    day_to_day_change = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    ema_12_day = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    ema_26_day = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    vol_ema = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    vol_avg_52_week = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    high_52_day = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    high_52_week = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    low_52_day = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    low_52_week = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    avg_52_day = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    avg_52_week = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    stdev_52_day = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)
    stdev_52_week = models.DecimalField(
        max_digits=15, decimal_places=4, default=0)

    def __str__(self):
        return str(self.company.name + " " + str(self.date))
        

    def __str__(self):
        return str(self.stock.name)