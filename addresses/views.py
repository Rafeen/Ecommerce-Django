from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import View
from .forms import AddressForm
from .models import Address
from billing.models import BillingProfile


class CheckOutAddressCreateView(View):
    """
     This view is for checkout address input
     and handles only post request
    """

    def post(self, request, *args, **kwargs):
        """
         post request inputs address for checkout process
        """
        form = AddressForm(request.POST or None)
        next_ = request.POST.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if form.is_valid():
            print(request.POST)
            instance = form.save(commit=False)  # saves model form
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if billing_profile is not None:
                """
                     associates address for logged in or guest user
                     and adds address id to session
                """
                address_type = request.POST.get('address_type', 'shipping')
                instance.billing_profile = billing_profile
                instance.address_type = address_type
                instance.save()
                request.session[address_type + '_address_id'] = instance.id
            else:
                return redirect('cart:checkout')

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('cart:checkout')
        return redirect('cart:checkout')


class CheckOutAddressReUseView(View):
    """
     This view is for checkout address reuse input
     and handles only post request
    """

    def post(self, request, *args, **kwargs):
        """
         post request inputs address for checkout process
        """
        if request.user.is_authenticated:
            print(request.POST)
            next_ = request.POST.get('next')
            next_post = request.POST.get('next')
            redirect_path = next_ or next_post or None

            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + '_address_id'] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)

        return redirect('cart:checkout')


