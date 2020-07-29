from django.contrib import admin
# Register your models here.
from . models import Product


class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'  # can also use updated field
    search_fields = ['title', 'description']
    list_display = ['id','__str__', 'price', 'active', 'updated']
    list_editable = ['price', 'active']
    list_filter = ['price', 'active']
    readonly_fields = ['slug', 'timestamp', 'updated']

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
