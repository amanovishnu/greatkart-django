from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'cart', 'quantity', 'is_active']
    list_display_links = ['product']

admin.site.register(CartItem, CartItemAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_id', 'date_added']
    list_display_links = ['id', 'cart_id']

admin.site.register(Cart, CartAdmin)
