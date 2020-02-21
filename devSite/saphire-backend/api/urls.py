from django.urls import path
from api import views

urlpatterns = [
    path('stocks/', views.stockList.as_view(), name='stockList'),
    path('stocks/<int:pk>/', views.stock.as_view(), name='stock'),
    path('stockChanges/', views.stockChangeList.as_view(), name='stockChangeList'),
    path('stockChanges/<int:pk>', views.stockChange.as_view(), name='stockChange'),
    path('users/', views.UserList.as_view(),name='userList'),
    path('users/<int:pk>/', views.User.as_view(), name='user')
]