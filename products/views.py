from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.shortcuts import Http404, HttpResponse

from .models import Product
from carts.models import Cart

# class HomeView(TemplateView):
#     template_name = "product/home_page.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Home'
#         context['product'] = Product.objects.all()
#
#         return context


class ProductFeaturedListView(ListView):
    """
     view for showing featured products list
    """
    model = Product
    queryset = Product.objects.featured()
    template_name = "products_list.html"
    context_object_name = 'product_list'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductFeaturedListView, self).get_context_data(*args, **kwargs)
        context['title'] = "Featured Products"
        return context


class ProductFeaturedDetailView(DetailView):
    """
      view for showing featured products details
     """
    model = Product
    queryset = Product.objects.featured()
    template_name = "featured_product_details.html"
    context_object_name = "product"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductFeaturedDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = "Product Details"
        return context


class ProductListView(ListView):
    """
      view for showing products list
     """
    model = Product
    template_name = "products_list.html"
    context_object_name = 'product_list'

    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        context['title'] = "Products"
        return context


class ProductDetailView(DetailView):
    """
      view for showing products detail
     """
    model = Product
    template_name = "product_details.html"
    context_object_name = 'product'

    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = "Product Details"
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj

        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug)
        except instance.DoesNotExist:
            raise Http404("Product doesn't exists")
        except instance.MultipleObjectsReturned:
            raise HttpResponse("Error Multiple Product Has Same SLUG")

        return instance
