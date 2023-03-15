from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'slug', 'price', 'stock', 'is_available', 'category', 'modified_date']
    list_display_links = ['product_name']
    prepopulated_fields = {
        'slug': ['product_name']
    }

admin.site.register(Product,ProductAdmin)
