from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from category.models import Category
from cart.models import CartItem
from .models import Product

from cart.views import _create_id


def store(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True).order_by('id')
        paginator = Paginator(products,3)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products,3)

    product_count = products.count()
    page = request.GET.get('page')
    try:
        paged_products = paginator.get_page(page)
    except PageNotAnInteger:
        paged_products = paged_products.get_page(1)
    except EmptyPage:
        paged_products = paged_products.get_page(paginator.num_pages)
    data ={
        'products':paged_products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context=data)



def product_detail(request, category_slug=None, product_slug=None):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _create_id(request), product=product).exists()
    except Exception as e:
        raise e
    data = {
        'product': product,
        'in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context=data)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('-created_date')
            product_count = products.count()
        data = {
            'products':products,
            'product_count': product_count
        }
    return render(request, 'store/store.html', context=data)
