from django.db import models

class Stock(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=200, default='', blank=True, null=True)
    vol = models.IntegerField()
    high = models.DecimalField(max_digits=4, decimal_places=2)
    low = models.DecimalField(max_digits=4, decimal_places=2)
    avg = models.DecimalField(max_digits=4, decimal_places=2)
    open = models.DecimalField(max_digits=4, decimal_places=2)
    close = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.name)

class StockChange(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=200, default='', blank=True, null=True)
    vol = models.IntegerField()
    high = models.DecimalField(max_digits=4, decimal_places=2)
    low = models.DecimalField(max_digits=4, decimal_places=2)
    avg = models.DecimalField(max_digits=4, decimal_places=2)
    open = models.DecimalField(max_digits=4, decimal_places=2)
    close = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.name)

