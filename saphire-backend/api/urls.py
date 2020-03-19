from django.urls import path
from api import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('stocks/', views.stockList.as_view(), name='stockList'),
    path('stocks/<int:pk>/', views.stock.as_view(), name='stock'),
    path('stockChanges/', views.stockChangeList.as_view(), name='stockChangeList'),
    path('stockChanges/<int:pk>/', views.stockChange.as_view(), name='stockChange'),
    path('users/', views.UserList.as_view(),name='userList'),
    path('users/<int:pk>/', views.User.as_view(), name='user'),
    path('watchStock/', views.WatchStock.as_view(), name='watchStock'),
    path('updateStock/', views.UpdateStock.as_view(), name='updateStock'),
    path('signIn/', views.Signin.as_view(), name='signIn'),
    path('signOut/', views.Signout.as_view(), name='signOut'),
    path('checkAuthenticated/', views.CheckAuthenticated.as_view(), name='checkAuthenticated'),
    
]