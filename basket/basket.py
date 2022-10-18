


class Basket():
    """
    Clase base del carrito de compras que provee ciertos comportamientos por defecto
    que se puede heredar o sobreescribir de ser necesario.
    """

    def __init__(self, request) -> None:
        
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket


    def add(self, product):
        """
        Agregar y actualizar la información de la sesion del carrito del usuario
        """
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = {'price': float(product.price)}
        
        self.session.modified = True
