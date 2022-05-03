from django.contrib import admin
from .models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug', 'price', 'stock', 'is_available', 'category', 'created_date', 'modified_date']
    prepopulated_fields = {
        'slug':('product_name',)
    }


admin.site.register(Product, ProductAdmin)


class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'created_date', 'is_active']
    list_filter = ['product', 'variation_category', 'variation_value']
    list_editable =  ['is_active']


admin.site.register(Variation, VariationAdmin)
