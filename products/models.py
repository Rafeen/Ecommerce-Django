import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.urls import reverse


def get_image_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance,filename):
    name, ext = get_image_ext(filename)
    instance_name = instance.title.replace(" ",'-')
    new_filename = random.randint(1,3910209312)
    final_filename = f"{instance_name}{new_filename}{ext}"
    return f"product/{instance_name}/{final_filename}"


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(active=True, featured=True)

    def search(self, query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(tag__title__icontains=query)
        )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def search(self, query):
        return self.get_queryset().search(query)

    def get_by_id(self, id):
        query = self.get_queryset().filter(id=id)
        if query.count() == 1:
            return query.first()
        else:
            return None


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    sale_price = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    objects = ProductManager()

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={"slug": self.slug})

    @property
    def name(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
