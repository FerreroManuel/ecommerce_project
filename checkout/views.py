import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from account.models import Address
from basket.basket import Basket
from orders.models import Order, OrderItem

from .mercado_pago import PAYMENT_STATUS, sdk
from .models import DeliveryOptions


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
    """
    Recibe la información del formulario de MercadoPago y lo guarda en la sesión
    """
    session = request.session

    user = request.user
    address = Address.objects.get(pk=request.session['address']['address_id'], customer=user)

    body = json.loads(request.body)

    payment_data = {
        "transaction_amount": float(body["transaction_amount"]),
        "token": body["token"],
        "description": 'MF! Store',
        "installments": int(body["installments"]),
        "payment_method_id": body["payment_method_id"],
        "payer": {
            "email": body["payer"]["email"],
            "identification": {
                "type": body["payer"]["identification"]["type"], 
                "number": body["payer"]["identification"]["number"],
                # "first_name": body["payer"]["first_name"],
                # "phone": {"number": int(address.phone_number)}
            },
        },
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    
    if 'mercadopago' not in request.session:
        session['mercadopago'] = {'response': payment}
    else:
        session['mercadopago']['response'] = payment
        session.modified = True

    return JsonResponse('Pago procesado', safe=False)


@login_required
def payment_response(request):
    """
    Elimina de la sesión la información del formulario de Mercadopago y actúa según
    el estado de la transacción:
    
    > Si fue aprobada registra en la base de datos la orden con sus respectivos productos,
    elimina toda la información de la compra de la sesión y dirige al usuario a lá página
    correspondiente.

    > Si no fue aprobada dirige al usuario a la página correspondiente.
    """

    session = request.session
    if 'mercadopago' in session:
        mp_response = session['mercadopago']['response']
        del session["mercadopago"]
        session.modified = True
    else:
        return redirect('account:orders')

    if mp_response["status"] == "approved":
        basket = Basket(request)
        user_id = request.user.id
        address = Address.objects.get(pk=session['address']['address_id'])

        order = Order.objects.create(
            user_id=user_id,
            email=mp_response["payer"]["email"],
            full_name=request.user.name,
            address1=address.address_line_1,
            address2=address.address_line_2,
            city=address.city,
            phone=address.phone_number,
            postal_code=address.postcode,
            country_code=address.country,
            total_paid=mp_response["transaction_details"]["total_paid_amount"],
            order_key=mp_response["id"],
            payment_option=mp_response["payment_type_id"],
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

        basket.clear()

        return render(request, 'checkout/payment_successful.html', {"order": order})
    else:
        if str(mp_response['status_detail']) in PAYMENT_STATUS:
            status_detail = PAYMENT_STATUS[str(mp_response['status_detail'])]
        else:
            status_detail = f'Error desconocido ({mp_response["status_detail"]})'
        
        message = f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi
        bi-x-circle-fill" viewBox="0 0 16 16">
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 
        2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 
        0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
        </svg>
        <b>Se produjo el siguiente error al intentar realizar el pago:</b>
        <ul><br><li>{status_detail}</li></ul>
        """
        messages.success(request, message)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
