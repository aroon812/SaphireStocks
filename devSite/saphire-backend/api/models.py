from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Stock(models.Model):
    watchedBy = models.ManyToManyField('UserProfile', blank=True, related_name='watchedStocks')
    date = models.DateField()
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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pk)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
