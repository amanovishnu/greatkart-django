from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Private Function to Create session as per PEP8 Guide
def _create_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_create_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _create_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_create_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_create_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request):
    total = 0
    tax = 0
    grand_total = 0
    total_quantity = 0
    try:
        cart = Cart.objects.get(cart_id=_create_id(request))
        cart_items =CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += item.product.price * item.quantity
            total_quantity += item.quantity
        tax = round(total*0.18,2) # 18% GST
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    data = {
        'total':total,
        'tax':tax,
        'grand_total': grand_total,
        'total_quantity': total_quantity,
        'cart_items': cart_items
    }
    return render(request, 'store/cart.html', context=data)
