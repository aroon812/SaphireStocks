from django.urls import path
from api.views import stocks
from core.views import index

urlpatterns = [
    path("stocks/", stocks, name="stocks"),
    path("", index, name="index")
]