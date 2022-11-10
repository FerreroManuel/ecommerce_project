import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        # Validations
        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, name, password, **other_fields)


    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    """
    Tabla de clientes. Por el momento los administradores/staff se crean
    también en esta tabla.
    """
    # Personal information
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=150)
    phone_number = PhoneNumberField(blank=True)

    # User status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Configuration data
    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"


    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            "contacto@manuelferrero.com.ar",
            [self.email],
            fail_silently=False,
        )


    def __str__(self):
        return self.name


class Address(models.Model):
    """
    Tabla de direcciones donde un cliente puede tener varias direcciones y teléfonos
    """
    # Sobreescritura del campo ID por defecto de Django por un campo UUID a fin de 
    # evitar el acceso público a información sensible de los usuarios a través del
    # uso aleatorio de slugs en el navegador
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full name"), max_length=150)
    phone_number = PhoneNumberField(blank=True)
    country = CountryField(blank=True)
    state = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    delivery_instructions = models.CharField(
        _("Delivery instructions"),
        max_length=255,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    
    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    
    def __str__(self):
        address = f"{self.address_line_1}"
        if self.address_line_2:
            address += f" {self.address_line_2}"
        return address
