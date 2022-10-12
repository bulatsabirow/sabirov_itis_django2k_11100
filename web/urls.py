from django.contrib import admin
from django.urls import path

from web.views import products_page, product_view, registration_view, authorization_view, add_product_view

urlpatterns = [
    path('products/', products_page, name='products'),
    path('product/<int:id>', product_view, name='product'),
    path('registration/', registration_view, name='register'),
    path('authorization/', authorization_view, name='auth'),
    path('add_product/', add_product_view, name='add'),
]