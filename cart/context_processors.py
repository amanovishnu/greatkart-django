from .models import Cart, CartItem
from .views import _create_id

def cart_counter(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id = _create_id(request))
            cart_items_count = CartItem.objects.filter(cart=cart).count()
        except Cart.DoesNotExist:
            cart_items_count = 0
        return dict(cart_items_count=cart_items_count)
