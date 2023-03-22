from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
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
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST.get(key)
            try:
                variation  = Variation.objects.get(product=product ,variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_create_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _create_id(request))
        cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        cart_item_id = []
        existing_variations_list = []
        for item in cart_item:
            cart_item_id.append(item.id)
            existing_variations = item.variations.all()
            existing_variations_list.append(list(existing_variations))
        if product_variation in existing_variations_list:
            idx = existing_variations_list.index(product_variation)
            item_id = cart_item_id[idx]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity+=1
            item.save()
        else:
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, id):
    cart = Cart.objects.get(cart_id=_create_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id ,id):
    cart = Cart.objects.get(cart_id=_create_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, id=id, cart=cart)
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
