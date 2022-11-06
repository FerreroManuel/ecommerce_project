from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_all(request):
    products = Product.products.all().order_by('-in_stock')
    return render(request, 'store/index.html', {'products': products})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(category=category).order_by('-in_stock')
    return render(request, 'store/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/product_detail.html', {'product': product})


def payment_methods(request):
    return render(request, 'store/payment_methods.html')
