from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    sale_price = models.DecimalField(decimal_places=2, max_digits=15, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return self.title

    def get_price(self):
        return self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField('products/images/')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title
