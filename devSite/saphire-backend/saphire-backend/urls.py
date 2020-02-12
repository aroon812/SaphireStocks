from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from api.views import stocks
from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('api.urls')),
    path("", index, name="index")
]