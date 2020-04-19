from django.urls import path
from api import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('stocks/', views.StockList.as_view(), name='stockList'),
    path('stocks/<int:pk>/', views.Stock.as_view(), name='stock'),
    path('stockChanges/', views.StockChangeList.as_view(), name='stockChangeList'),
    path('stockChanges/<int:pk>/', views.StockChange.as_view(), name='stockChange'),
    path('users/', views.UserList.as_view(),name='userList'),
    path('users/<int:pk>/', views.User.as_view(), name='user'),
    path('companies/', views.CompanyList.as_view(), name='companyList'),
    path('companies/<int:pk>/', views.Company.as_view(), name='company'),
    path('users/<int:pk>/changePassword/', views.change_password, name='passwordChange'),
    path('watchStock/', views.WatchStock.as_view(), name='watchStock'),
    path('updateStock/', views.UpdateStock.as_view(), name='updateStock'),
    path('watchedList/', views.getWatchedStocks.as_view(), name='watchedList'),
    #path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), 
]