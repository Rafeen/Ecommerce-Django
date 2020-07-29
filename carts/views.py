from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Cart
from products.models import Product


class CartView(View):
    template_name = "cart.html"

    def get(self, request, *args, **kwargs):
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        context = {
            'cart': cart_obj
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        request = self.request
        product_id = request.POST.get('product_id')

        if product_id is not None:
            try:
                product_obj = Product.objects.get_by_id(product_id)
            except Product.DoesNotExist:
                print('poof!! product is gone')
                return redirect('cart:cart-product')

            cart_obj, new_obj = Cart.objects.new_or_get(request)
            if product_obj in cart_obj.products.all():
                cart_obj.products.remove(product_obj)
            else:
                cart_obj.products.add(product_obj)
            request.session['cart_items'] = cart_obj.products.count()

        return redirect('cart:cart-product')




