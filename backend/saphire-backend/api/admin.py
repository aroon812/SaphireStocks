from django.contrib import admin
from .models import Stock, StockChange, Company, User

admin.site.register(User)
admin.site.register(Stock)
admin.site.register(StockChange)
admin.site.register(Company)

