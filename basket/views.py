from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .basket import Basket


def basket_summary(request):
    return render(request, 'basket/basket.html')


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basket_qty = len(basket)
        response = JsonResponse({'qty': basket_qty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product_id=product_id)
        basket_qty = basket.__len__()
        basket_subtotal = basket.get_subtotal_price()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_subtotal, 'total': basket_total})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product_id=product_id, product_qty=product_qty)
        basket_qty = basket.__len__()
        basket_subtotal = basket.get_subtotal_price()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_subtotal, 'total': basket_total})
        return response
