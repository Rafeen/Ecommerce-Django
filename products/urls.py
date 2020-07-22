from django.contrib import admin
from django.urls import path, include
from .views import HomeView, AllProducts

app_name = "products"
urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('products/', AllProducts.as_view(), name='products'),

]