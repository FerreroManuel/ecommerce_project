from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Tabla de categorías implementada con MPTT
    """
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Category safe URL"),
        max_length=255,
        unique=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    is_active = models.BooleanField(default=True)


    class MPTTMeta:
        order_insertion_by = ["name"]


    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])


    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    Tabla de tipo de producto que provee una lista de los diferentes tipos
    de productos que hay a la venta.
    """
    name = models.CharField(
        verbose_name=_("Product Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")


    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    Tabla de especificación de producto que contiene las especificaciones o
    características de los tipos de productos.
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_("Name"),
        help_text=_("Required"),
        max_length=255,
    )
    
    
    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")
    
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Tabla productos que contiene todos los productos
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Not required"),
        blank=True
    )
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular Price"),
        help_text=_("Max. 999999999.99"),
        error_messages={
            "Name": {
                "max_length": _("The price must be between 0 and 999999999.99.")
            }
        },
        max_digits=11,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount Price"),
        help_text=_("Max. 999999999.99"),
        error_messages={
            "Name": {
                "max_length": _("The price must be between 0 and 999999999.99.")
            }
        },
        max_digits=11,
        decimal_places=2,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    
    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])


    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    """
    Tabla de valor de especificación de producto que contiene cada una de
    las especificaciones o características de cada producto individual.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Product specification value (max. of 255 characters)"),
        max_length=255,
    )


    class Meta:
        verbose_name = _("Product specification value")
        verbose_name_plural = _("Product specification values")
    

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    Tabla de imágenes de producto
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/no-disponible.jpg",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
