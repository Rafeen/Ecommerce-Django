from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Cart
from addresses.models import Address
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile

from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm


class CartView(View):
    """
    cart view
    """
    template_name = "cart.html"

    def get(self, request, *args, **kwargs):
        """
        For get request only renders the cart with items
        """
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        context = {
            'cart': cart_obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
              For post requests adds products to the cart
             or removes products from the cart if already exists n the cart
        """
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


def checkout_process_view(request):
    """
     change order status to done after checking out
     when order is checked out cart id in the session should be cleared
     redirect to success
     """
    template_name = 'checkout.html'
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:cart-product')

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        "check that order is done"
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect('cart:checkout-done')
    context = {
        'order': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
    }
    return render(request, template_name, context)


def checkout_success_view(request):
    template_name = 'checkout-done.html'
    context = {}
    return render(request, template_name, context)



