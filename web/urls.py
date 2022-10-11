from django.contrib import admin
from django.urls import path

from web.views import products_page

urlpatterns = [
    path('main/', products_page, name='products')
]