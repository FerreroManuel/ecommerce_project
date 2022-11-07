from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from basket.basket import Basket
from account.models import UserBase
from .forms import OrderForm
from .models import Order, OrderItem


@login_required(login_url=reverse_lazy('account:login'))
def order(request):
    if request.method == 'POST':
        return add(request)
    else:
        user = get_object_or_404(UserBase, user_name=request.user)
        if user.first_name and user.last_name:
            full_name = f'{user.first_name} {user.last_name}'
        else:
            full_name = None
        basket = Basket(request)
        total = basket.get_total_price()
        order_form = OrderForm(data={
            'full_name': full_name,
            'address1': user.address_line_1,
            'address2': user.address_line_2,
            # 'city': user.city,                # Sólo envíos a Rosario x el momento (cambiar forms si se activa)
            'city': 'Rosario',
            'phone': user.cell_phone,
            'postcode': user.postcode,
            'total_paid': total,
        })
        return render(request, 'orders/order.html', {'order_form': order_form})


def add(request):
    basket = Basket(request)
    if request.method == 'POST':
        user_id = request.user.id
        user = get_object_or_404(UserBase, id=user_id)
        basket_total = basket.get_total_price()
        order = Order.objects.create(                   # <------ ELIMINAR CUANDO HAGA EL IF RETIRO/ENVIO
            user=user,
            full_name=request.POST.get('full_name'),
            # address1=request.POST.get('address1'),
            address1='No aplica',                       # <------ ELIMINAR CUANDO HAGA EL IF RETIRO/ENVIO
            # address2=request.POST.get('address2'),
            address2='No aplica',                       # <------ ELIMINAR CUANDO HAGA EL IF RETIRO/ENVIO
            # city=request.POST.get('city'),
            city='No aplica',                           # <------ ELIMINAR CUANDO HAGA EL IF RETIRO/ENVIO
            phone=request.POST.get('phone'),
            # postcode=request.POST.get('postcode'),
            postcode='No aplica',                       # <------ ELIMINAR CUANDO HAGA EL IF RETIRO/ENVIO
            total_paid=basket_total,
        )
        order_id = order.pk
        order_items = basket
        basket.clear()
        for item in order_items:
            OrderItem.objects.create(
                order_id=order_id,
                product=item['product'],
                price=item['price'],
                quantity=item['qty'],
            )

        # Setup confirmation email
        current_site = get_current_site(request)
        subject = 'Pedido confirmado | BookStore'
        message = render_to_string(
            'orders/order_confirmation_email.html',
            {
                'domain': current_site.domain,
                'user': user,
                'order': order,
            },
        )
        user.email_user(subject=subject, message=message)
    return render(request, 'orders/order_confirm.html')


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=False)
    orders_paid = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders, orders_paid


"""

ESTOY BUSCANDO QUE DESDE 'MI CARRITO', AL PRESIONAR SOBRE 'REALIZAR COMPRA', ME LLEVE A UN FORMULARIO
DE ENVÍO Y CONFIRMACIÓN DE LA ORDEN. UNA VEZ QUE SE ENVÍE EL FORMULARIO SE DEBE CREAR UNA ORDEN Y DESPUÉS
ENVIAR UN EMAIL AL CLIENTE Y EL VENDEDOR CON LOS DATOS DE ÉSTA.

DESPUÉS, SI EL VENDEDOR RECIBE EL PAGO, TIENE QUE MARCAR LA ORDEN COMO PAGA Y ADJUNTARLE NRO. DE RECIBO O
DE TRANSFERENCIA.

"""
