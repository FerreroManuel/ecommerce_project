from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryOptions(models.Model):
    """
    Tabla de opciones de envío
    """

    DELIVERY_CHOICES = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery"),
    ]
    
    delivery_name = models.CharField(
        verbose_name=_("Delivery name"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_price = models.DecimalField(
        verbose_name=_("Delivery price"),
        help_text=_("Max. 99999.99"),
        error_messages={
            'name': {
                'max_length': _("The price must be between 0 and 99999.99"),
            },
        },
        max_digits=7,
        decimal_places=2
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES,
        verbose_name=_("Delivery method"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_timeframe = models.CharField(
        verbose_name=_("Delivery timeframe"),
        help_text=_("Required"),
        max_length=255,
    )
    delivery_window = models.CharField(
        verbose_name=_("Delivery window"),
        help_text=_("Required"),
        max_length=255,
    )
    order = models.IntegerField(
        verbose_name=_("List order"),
        help_text=_("Required"),
        default=0,
    )
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = _("Delivery option")
        verbose_name_plural = _("Delivery options")

    
    def __str__(self):
        return self.delivery_name


class PaymentSelections(models.Model):
    """
    Tabla de métodos de pago
    """
    
    name = models.CharField(
        verbose_name=_("Name"),
        help_text=_("Required"),
        max_length=255,
    )
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = _("Payment selection")
        verbose_name_plural = _("Payment selections")

    
    def __str__(self):
        return self.name
