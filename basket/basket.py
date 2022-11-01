from decimal import Decimal
from django.conf import settings
from store.models import Product


class Basket():
    """
    Clase base del carrito de compras que provee ciertos comportamientos por defecto
    y se puede heredar o sobreescribir de ser necesario.
    """

    def __init__(self, request) -> None:

        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        self.shipping = Decimal(0.00)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket


    def add(self, product, qty):
        """
        Agrega y actualiza la información de la sesión del carrito del usuario
        """
        product_id = str(product.id)

        if product_id not in self.basket:
            self.basket[product_id] = {'price': float(product.price), 'qty': int(qty)}
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
        Obtiene los totales de todos los productos y devuelve el total
        """
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        

    def get_total_price(self):
        """
        Obtiene el subtotal, le suma el envío y devuelve el total
        """
        subtotal = self.get_subtotal_price()
        if subtotal == 0:
            total = Decimal(0.00)
        else:
            total = subtotal + Decimal(self.shipping)
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
        self.save_session()


    def __iter__(self):
        """
        Recoge los product_id en la información de la sesión para hacer un query en la base de datos
        y retornar los productos como iterable
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
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
