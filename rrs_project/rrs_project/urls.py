from django.contrib import admin
from django.urls import path, include
from rrs_app import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('rrs_app.urls')),
]
