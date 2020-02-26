from django.contrib import admin
from .models import Stock, StockChange, User

admin.site.register(Stock)
admin.site.register(StockChange)
admin.site.register(User)

