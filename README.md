# English

## Ecommerce website project using Django

This repository contains a project where was developed a generic website with ecommerce using Django library for Python.

The project consists of a store website, through which clients can make purchases online.

### Users:

> Both clients and staff members have a user account through which they can carry out their operations, whether it is the purchase of products or the administration of the site, in case of being a member of the staff.
>
> All users must register through a registration form, providing an email address, first name, last name and password. Except for email, all data can be edited at any time if the user wishes.
>
> In case of forgetting the password, users can request its reset through the web. Once requested, an email will be sent to the email account provided by the user at the time of registration, in which will be provided a single access link to a password reset form.
>
> If desired, the user can request the deletion of his account, which will be disabled immediately. At the moment only the irrevocable deactivation of the account is carried out, however the data is still stored in the database. In future updates, the entire account deletion circuit will be reconsidered to improve this aspect of personal data management.

### Addresses:

> A user can add as many addresses as he wishes. Each address has a person responsible for receiving the purchase, a telephone number and the possibility of adding special instructions for delivery.
>
> Users can edit or delete the registered addresses at any time they want.

### Wishlist:

> Users have the ability to add or remove products from their wishlist, and access them at any time without having to search for.

### Products:

> All products have the following characteristics:
> - Product type
> - Category (Sub-categories can be created)
> - Title or name of the product
> - Product description
> - Regular price of the product
> - Discounted price
> - Product images
> - Special features of the product type (exclusive features can be added or removed for each product type)
> - Status (Active / Inactive)
> - Product creation date
> - Product edition date

### Basket:

> Through the use of the context processor, users are allowed to add and remove products from the shopping basket. It is saved in the session and stores the information of the products and quantities that the user adds to the basket, the type of shipment and the address chosen by the user.
>
> Besides, it can connect to the database and, based on the stored data, calculate the total and subtotal prices of the purchase.

### Shipping:

> The site administrator can make different types of shipments available to users with individual costs for each one. The user, on the other hand, can choose the type of shipment he wishes for his purchase and, depending on whether it is a shipment or a pickup in store, select his own address or the store address respectively.

### Payments:

> The site accepts payments with debit and credit cards through the use of the mercadopago's SDK. Once a purchase is completed, the form is loaded to make a secure payment through the technology provided by Mercado Pago.

### Orders:

> Once the purchase is complete, both the user and the site administrator receive an email with the details corresponding to the order. The user can see the details of the orders placed through the website.

### Site administration:

> Site administration is done through the administration site provided by Django. The access is restricted to users who belong to the staff.

<br>

## Future updates

- Incorporation of cash payment option
- Incorporation of a shipping cost model by location.
- Incorporation of digital shipments.
- Re-adaptation of product models to be able to offer suitable types of shipment for each type of product.
- Incorporation of a workflow system for the staff members to operate with the orders made by the users.
- Restructuring of the user account deletion circuit.
- Front-end refactoring

# Developer

The website was developed by Manuel Ferrero for MF! Soluciones Informáticas.

## Contact information

- Telephone: ```+543413712406```
- Email: ```contacto@manuelferrero.com.ar```
- Web: ```www.manuelferrero.com.ar```

<br>
<br>
<br>

# Español

## Sitio web con ecommerce usando Django

Este repositorio contiene un proyecto en el cual se desarrolló un sitio web con ecommerce utilizando la librería Django de Python.

El proyecto consiste en un sitio web genérico para utilizar en una tienda, mediante la cual los clientes pueden realizar compras de manera online.

### Usuarios:

> Tanto clientes como miembros del staff poseen un cuenta de usuario mediante la cuál pueden realizar sus operaciones, ya sea la compra de productos o la administración del sitio, en caso de ser miebro del staff.
>
> Todos los usuarios deben registrarse mediante un formulario de registro, brindando una dirección de email, nombre, apellido y contraseña. A excepción del email, todos los datos pueden ser editados en cualquier momento si el usuario lo desea.
>
> En caso de olvidar la contraseña los usuarios pueden pedir el reestablecimiento de la misma a través de la web. Una vez solicitado se enviará un correo electrónico a la cuenta de email proporcionada por el usuario al momento de registrarse, en el cual se le brindará un link de acceso único hacia un formulario de reestablecimiento de contraseña.
>
> Si lo deseara, el usuario puede solicitar la eliminación de su cuenta, la cual será inhabilitada de inmediato. Por el momento sólo se realiza la inactivación irrevocable de la cuenta, sin embargo los datos se siguen almacenando en la base de datos. En próximas actualizaciones se replanteará todo el circuito de eliminación de cuentas para mejorar este aspecto del manejo de datos personales.

### Domicilios:

> Un usuario puede agregar tantos domicilios como desee. Cada domicilio posee una persona responsable de recibir la compra, un número de teléfono y la posibilidad de agregar instrucciones especiales para la entrega.
>
> El usuario puede editar o eliminar los domicilios registrados en cualquier momento que lo desee.

### Favoritos:

> Los usuarios tienen la posibilidad de agregar o eliminar productos de su lista de favoritos, y acceder a ellos en cualquier momento sin necesidad de buscarlos.

### Productos:

> Todos los productos tienen las siguientes características:
> - Tipo de producto
> - Categoría (Pueden crearse sub-categorías)
> - Título o nombre del producto
> - Descripción del producto
> - Precio regular del producto
> - Precio con descuento
> - Imágenes del producto
> - Características especiales del tipo de producto (se pueden agregar o quitar características exclusivas para cada tipo de producto)
> - Estado (Activo / Inactivo)
> - Fecha de creación del producto
> - Fecha de edición del producto

### Carrito:

> A través del uso del procesador de contexto, se le permite a los usuarios agregar y quitar productos del carrito de compras. El mismo se guarda en la sesión y almacena la información de los productos y cantidades que el usuario agrega al carrito de compras, el tipo de envío y el domicilio elegidos por el usuario.
>
> A su vez se puede conectar con la base de datos y, a partir de los datos alamacenados, calcular los precios totales y subtotales de la compra.

### Envíos:

> El administrador del sitio puede poner a disposición de los usuarios distintos tipos de envíos con costos individuales para cada uno. El usuario, por su parte, puede escoger el tipo de envío que desea para su compra y, dependiendo si es un envío o un retiro, seleccionar un domicilio propio o del negocio respectivamente.

### Pagos:

> El sitio acepta pagos con tarjetas de débito y crédito mediante el uso de el SDK de mercadopago. Una vez finalizado una compra, se procede a cargar el formulario para realizar un pago seguro a través de la tecnología brindada por Mercado Pago.

### Pedidos:

> Una vez finalizada la compra, tanto el usuario como el administrador del sitio recibe un correo electrónico con los detalles correspondientes al pedido. El usuario puede ver el detalle de los pedidos realizados a través del sitio web.

### Adiministración del sitio:

> La administración del sitio se realiza a través del sitio de administración que provee Django. El mismo se encuentra restringido a usuarios que pertenezcan al staff.

<br>

## Futuras actualizaciones

- Incorporación de sistema de pago en efectivo
- Incorporación de un modelo de costos de envíos según localidad.
- Incorporación de envíos digitales.
- Re-adaptación de modelos de productos para poder ofrecer tipo de envío adecuados para cada tipo de producto.
- Incorporación de sistema de workflow para que los miembros del staff operen con los pedidos realizados por los usuarios.
- Re-estructuración del circuito de eliminación de cuentas de usuario.
- Refactorización del front-end

# Desarrollador

El sitio web fue desarrollado por Manuel Ferrero para MF! Soluciones Informáticas.

## Datos de contacto

- Teléfono: ```+543413712406```
- Email: ```contacto@manuelferrero.com.ar```
- Web: ```www.manuelferrero.com.ar```

<br>
<br>
<br>
