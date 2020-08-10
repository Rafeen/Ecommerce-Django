from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail


class CartView(View):
    template_name = "cart.html"

    def get(self, request, *args, **kwargs):
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        context = {
            'cart': cart_obj,
            'tax': cart_obj.total - cart_obj.subtotal
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


def checkout(request):
    template_name = 'checkout.html'
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:cart-product')
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass
    context = {
        'order': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
    }
    return render(request, template_name, context)




