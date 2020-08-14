from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES_CHOICES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES_CHOICES)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        address = f"{self.address_line_1}\n{self.address_line_2}\n{self.city},{self.postal_code}\n{self.country}".replace("None", "")
        return address
