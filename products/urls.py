from django.contrib import admin
from django.urls import path, include
from .views import (
        ProductListView,
        ProductDetailView,
        # ProductFeaturedListView,
        # ProductFeaturedDetailView
)

app_name = "products"
urlpatterns = [

    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    # path('featured/', ProductFeaturedListView.as_view(), name='featured-product-list'),
    # path('featured/<int:pk>', ProductFeaturedDetailView.as_view(), name='featured-product-detail'),

]