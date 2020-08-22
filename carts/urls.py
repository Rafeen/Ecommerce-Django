from django.contrib import admin
from django.urls import path, include
from .views import CartView, checkout_process_view, checkout_success_view, cart_update_api_view

app_name = "cart"
urlpatterns = [

    path('', CartView.as_view(), name='cart-product'),
    path('api/', cart_update_api_view, name='cart-api'),
    path('checkout/', checkout_process_view, name='checkout'),
    path('checkout/success', checkout_success_view, name='checkout-success'),
    path('checkout/', include('addresses.urls', namespace='address')),

]
