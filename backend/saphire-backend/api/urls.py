from django.urls import path
from api import views


urlpatterns = [
    path('stocks/', views.StockList.as_view(), name='stockList'),
    path('stocks/<int:pk>/', views.Stock.as_view(), name='stock'),
    path('stocks/stockRange/', views.stock_range, name='stockRange'),
    path('stocks/recentInfo/', views.recent_stock_info, name='recentInfo'),
    path('companies/', views.CompanyList.as_view(), name='companyList'),
    path('companies/<str:pk>/', views.Company.as_view(), name='company'),
    path('search/', views.search, name='search'),
    path('watchStock/', views.WatchStock.as_view(), name='watchStock'),
    path('watchedList/', views.GetWatchedStocks.as_view(), name='watchedList'),
]