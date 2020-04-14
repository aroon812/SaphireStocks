from django.contrib import admin
from .models import Stock, StockChange, User, Company

admin.site.register(Stock)
admin.site.register(StockChange)
admin.site.register(User)
admin.site.register(Company)

