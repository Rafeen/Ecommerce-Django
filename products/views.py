from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from .models import Product


# class HomeView(TemplateView):
#     template_name = "products/home.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Home'
#         context['products'] = Product.objects.all()
#
#         return context


class AllProducts(ListView):
    model = Product
    template_name = "products/products_list.html"
    context_object_name = 'products'
