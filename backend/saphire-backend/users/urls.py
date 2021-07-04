from django.urls import path 
from users.views import APILoginView, APILogoutView, APIPasswordUpdateView
from users import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', APILoginView.as_view(), name='api_login'),
    path('logout/', APILogoutView.as_view(), name='api_logout'),
    path('update_password/', APIPasswordUpdateView.as_view(), name='api_update_password'),
    path('users/', views.UserList.as_view(),name='userList'),
    path('users/current_user/', views.CurrentUser.as_view(), name='current_user'),
    path('users/<int:pk>/', views.User.as_view(), name='user'),
]