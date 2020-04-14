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
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    watchedStocks = models.ManyToManyField('Company', blank=True, related_name='watchedBy')
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
    symbol = models.CharField(max_length=5, default='', blank=True, null=False, unique=True, primary_key=True)
    name = models.CharField(max_length=200, default='', blank=True, null=True)
    
    def __str__(self):
        return str(self.name)

class Stock(models.Model):
    date = models.DateField()
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    vol = models.IntegerField()
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    avg = models.DecimalField(max_digits=10, decimal_places=4)
    open = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return str(self.company.name + " " + str(self.date))

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