import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from paypalcheckoutsdk.orders import OrdersGetRequest

from account.models import Address
from basket.basket import Basket
from orders.models import Order, OrderItem

from .models import DeliveryOptions, PaymentSelections
from .paypal import PayPalClient


@login_required(login_url=reverse_lazy("account:login"))
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True).order_by('order')
    return render(request, 'checkout/delivery_choices.html', {'deliveryoptions': deliveryoptions})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if 'purchase' not in session:
            session['purchase'] = {
                'delivery_id': delivery_type.id,
            }
        else:
            session['purchase']['delivery_id'] = delivery_type.id
            session.modified = True

        response = JsonResponse({'total': updated_total_price, 'delivery_price': delivery_type.delivery_price})
        return response


@login_required
def delivery_address(request):
    session = request.session
    if 'purchase' not in session:
        messages.success(request, 'Por favor seleccione un tipo de envío')
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    if 'address' not in request.session:
        session['address'] = {'address_id': str(addresses[0].id)}
    else:
        session['address']['address_id'] = str(addresses[0].id)
        session.modified = True

    return render(request, 'checkout/delivery_address.html', {"addresses": addresses})
        


@login_required
def payment_selection(request):
    if 'address' not in request.session:
        messages.success(request, 'Seleccione una dirección de envío')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return render(request, 'checkout/payment_selection.html', {})


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    
    data = body['OrderID']
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    purchase_units = response.result.purchase_units[0]
    total_paid = purchase_units.amount.value

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=purchase_units.shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=purchase_units.shipping.address.address_line_1,
        address2=purchase_units.shipping.address.admin_area_2,
        postal_code=purchase_units.shipping.address.postal_code,
        country_code=purchase_units.shipping.address.country_code,
        total_paid=total_paid,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(
            order_id=order_id,
            product=item['product'],
            price=item['price'],
            quantity=item['qty'],
        )
    
    return JsonResponse('Pago realizado con éxito!', safe=False)


@login_required
def payment_succesful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'checkout/payment_successful.html', {})
