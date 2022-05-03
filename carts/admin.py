from django.contrib import admin
from . import models

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']


admin.site.register(models.Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'is_active']


admin.site.register(models.CartItem, CartItemAdmin)
