from django.contrib import admin
from django.urls import path, include
from .views import AllProducts

app_name = "products"
urlpatterns = [

    path('', AllProducts.as_view(), name='products'),

]