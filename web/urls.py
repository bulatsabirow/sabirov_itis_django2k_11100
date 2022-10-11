from django.contrib import admin
from django.urls import path

from web.views import products_page, product_view

urlpatterns = [
    path('products/', products_page, name='products'),
    path('product/<int:id>', product_view, name='product'),
]