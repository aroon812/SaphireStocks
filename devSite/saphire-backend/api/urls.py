from django.urls import path
from api import views

urlpatterns = [
    path('stocks/', views.stockList, name='stockList'),
    path('stocks/<int:pk>/', views.stock, name='stock'),
    path('stockChanges/', views.stockChangeList, name='stockChangeList'),
    path('stockChanges/<int:pk>', views.stockChange, name='stockChange'),
    path('users/<int:pk>/', views.user, name='user')
]