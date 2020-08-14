
from django.urls import path
from .views import CheckOutAddressCreateView, CheckOutAddressReUseView

app_name = "address"

urlpatterns = [
    path('address/create/', CheckOutAddressCreateView.as_view(), name="address-create"),
    path('address/reuse/', CheckOutAddressReUseView.as_view(), name="address-reuse"),

]