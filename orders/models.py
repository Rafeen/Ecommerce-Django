import math
from django.db import models
from django.db.models.signals import pre_save, post_save
from billing.models import BillingProfile
from carts.models import Cart
from Ecommerce.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        """
         This is a custom query for creating
         new order or get existing order object
        """
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile,
                                        cart=cart_obj,
                                        active=True)
        if qs.count() == 1:
            created = False
            obj = qs.first()
        else:
            obj = self.models.objects.create(billing_profile=billing_profile,
                                             cart=cart_obj)
            created = True

        return obj, created


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    # billing_address =
    # shipping_address =
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    object = OrderManager

    def update_total(self):
        """
         calculates order total and updates it
        """
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        new_total = format(new_total, '.2f')
        self.total = new_total
        self.save()
        return new_total


def pre_save_create_order_id(sender, instance,*args, **kwargs):
    """
     this pre_save signal creates a unique order id
     for new order and deactivates pre-existing order with same cart object
    """
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, *args, **kwargs):
    """
     this pre_save signal updates order total when
     there is a change in the associated cart
    """
    cart_obj = instance
    cart_total = cart_obj.total
    cart_id = cart_obj.id
    qs = Order.objects.filter(cart__id=cart_id)
    if qs.count() == 1:
        order_obj = qs.first()
        order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    """
     this post_save signal updates
     order total at hte time of creation
    """
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
