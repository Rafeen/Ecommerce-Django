from django.contrib import admin
from django.urls import path, include
from .views import CartView

app_name = "cart"
urlpatterns = [

    path('', CartView.as_view(), name='cart-product'),

]
