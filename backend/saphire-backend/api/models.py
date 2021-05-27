from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, BaseUserManager


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates a superuser that can authenticate by email instead of username.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    A user object which is a modified version of the base Django user.
    """
    watchedStocks = models.ManyToManyField(
        'Company', blank=True, related_name='watchedBy')
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


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


class StockChange(models.Model):
    """
    Represents the normalized data for each stock, which is used as input data for machine learnign models.
    """
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    date = models.DateField(null=False)
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
        return str(self.stock.name)