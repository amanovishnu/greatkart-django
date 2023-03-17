from django.contrib import admin
from .models import Product, Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'slug', 'price', 'stock', 'is_available', 'category', 'modified_date']
    list_display_links = ['product_name']
    prepopulated_fields = {
        'slug': ['product_name']
    }

admin.site.register(Product,ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'variation_category', 'variation_value', 'is_active', 'created_date']
    list_display_links = ['product']
    list_editable = ['is_active']
    list_filter = ['product', 'variation_category', 'variation_value']

admin.site.register(Variation,VariationAdmin)
