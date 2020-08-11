from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product


class SearchProductListView(ListView):
    """
      view for showing searched products list
     """
    model = Product
    template_name = "search_view.html"
    context_object_name = 'product_list'

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query=query)
        else:
            return Product.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        context['title'] = f"Search results for {self.request.GET.get('q').upper()}"
        context['query'] = self.request.GET.get('q')
        return context
