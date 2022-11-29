from decimal import Decimal

from django.conf import settings

from checkout.models import DeliveryOptions
from store.models import Product


class Basket():
    """
    Clase base del carrito de compras que provee ciertos comportamientos por defecto
    y se puede heredar o sobreescribir de ser necesario.
    """

    def __init__(self, request) -> None:

        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket


    def add(self, product, qty):
        """
        Agrega y actualiza la información de la sesión del carrito del usuario
        """
        product_id = str(product.id)

        if product_id not in self.basket:
            self.basket[product_id] = {'price': float(product.regular_price), 'qty': int(qty)}
        else:
            self.basket[product_id]['qty'] += int(qty)
        self.save_session()


    def delete(self, product_id):
        """
        Borra y actualiza la información de la sesión del carrito
        """
        product_id = str(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save_session()


    def update(self, product_id, product_qty):
        """
        Actualiza la cantidad de un producto en de la sesión del carrito
        """
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
        self.save_session()


    def get_subtotal_price(self):
        """
        Obtiene los totales de todos los productos y retorna el total
        """
        subtotal = sum(item['price'] * item['qty'] for item in self.basket.values())
        return Decimal(subtotal)


    def get_delivery_price(self):
        """
        Obtiene el precio del envío de la sesión y lo retorna
        """
        if 'purchase' in self.session:
            delivery_price = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price
        else:
            delivery_price = 0
        return Decimal(delivery_price)


    def get_total_price(self):
        """
        Obtiene el subtotal, le suma el envío y retorna el total
        """
        subtotal = self.get_subtotal_price()
        if 'purchase' in self.session:
            shipping = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price
        else:
            shipping = Decimal(0)
        total = subtotal + Decimal(shipping)
        return Decimal(total)


    def basket_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    
    def save_session(self):
        """
        Guarda la sesión
        """
        self.session.modified = True


    def clear(self):
        """
        Elimina el carrito de la sesión
        """
        del self.session[settings.BASKET_SESSION_ID]
        del self.session["address"]
        del self.session["purchase"]
        self.save_session()


    def __iter__(self):
        """
        Recoge los product_id en la información de la sesión para hacer un query en la base de datos
        y retornar los productos como iterable
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['total_price'] = float(item['price'] * item['qty'])
            yield item


    def __len__(self):
        """
        Obtiene la información del carrito y cuenta la cantidad de items
        """
        return sum(item['qty'] for item in self.basket.values())
