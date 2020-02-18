from django.contrib import admin
from .models import Stock, StockChange, UserProfile

admin.site.register(Stock)
admin.site.register(StockChange)
admin.site.register(UserProfile)
