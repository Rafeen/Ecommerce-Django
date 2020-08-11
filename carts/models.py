from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        """
         creates new cart or gets existing cart
         if user is authenticated then assign cart
         to the user from session
        """
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                # Cart.objects.filter(user=request.user).delete()  # one user should have only one cart
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = self.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        """
         creates new cart for user object
        """
        user_obj = None
        if user is not None and user.is_authenticated:
            user_obj = user
        return self.get_queryset().create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    """
     this m2m_changed signal updates cart total
     after adding or removing each product
    """
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        cart = instance.products.all()
        total = 0
        for product in cart:
            total += product.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    """
     this pre_save signal updates
     subtotal with 5% tax calculation
    """
    if instance.subtotal > 0:
        instance.total = format(Decimal(instance.subtotal) * Decimal(1.05), '.0f')    # 5% tax
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)

