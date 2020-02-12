from django.urls import path
from api.views import stocks

urlpatterns = [
    path('stocks/', stocks, name='stocks'),
]