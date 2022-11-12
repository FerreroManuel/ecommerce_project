from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.modelfields import PhoneNumberField

from .models import Address, Customer


class RegistrationForm(forms.ModelForm):

    email = forms.EmailField(
        max_length=100,
        help_text="*",
        error_messages={
            "required": _("Email field is required"),
        },
    )
    name = forms.CharField(
        label=_("Name"),
        min_length=4,
        max_length=50,
        help_text="*",
        error_messages={
            "required": _("Name field is required"),
        },
    )
    phone_number = PhoneNumberField().formfield(
        label=_("Phone number"),
        help_text="*",
        error_messages={
            "required": _("Phone number field is required"),
        },
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(),
        error_messages={
            "required": _("Password field is required"),
        },
    )
    password2 = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput(),
        error_messages={
            "required": _("Repeat password field is required"),
        },
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control mb3",
                "placeholder": "Email",
                "id": "email",
            }
        )
        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control mb3",
                "placeholder": _("Name"),
                "id": "name",
            }
        )
        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "form-control mb3",
                "placeholder": _("Phone number"),
                "id": "phone_number",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control mb3",
                "placeholder": _("Password"),
                "id": "password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control mb3",
                "placeholder": _("Repeat password"),
                "id": "password2",
            }
        )


    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError(_("Passwords don't match"))
        return cd["password2"]


    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(_("The email is already registered in our database"))
        return email


    class Meta:
        model = Customer
        fields = ("name", "email", "phone_number")


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "email",
            },
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("Password"),
                "id": "login-pwd",
            },
        ),
    )


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label="Email",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": "Email",
                "id": "form-email",
                "readonly": "readonly",
            },
        ),
    )
    name = forms.CharField(
        label=_("Name"),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("Name"),
                "id": "form-name",
            },
        ),
    )
    phone_number = PhoneNumberField().formfield(
        label=_("Phone number"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("Phone number"),
                "id": "form-phone_number",
            },
        ),
    )


    class Meta:
        model = Customer
        fields = (
            "email",
            "name",
            "phone_number",
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["name"].required = True
        self.fields["phone_number"].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Email", "id": "form-email"}),
    )


    def clean_email(self):
        email = self.cleaned_data["email"]
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(_("The email is not registered in our database"))
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": _("New password"), "id": "form-newpass1"}
        ),
    )
    new_password2 = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": _("Repeat password"), "id": "form-newpass2"}
        ),
    )


class PwdChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": _("Old password"), "id": "form-oldpass"}
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": _("New password"), "id": "form-newpass1"}
        ),
    )
    new_password2 = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": _("Repeat password"), "id": "form-newpass2"}
        ),
    )


class UserAddressForm(forms.ModelForm):
    full_name = forms.CharField(
        label=_("Full name"),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("Full name"),
                "id": "form-full-name",
            },
        ),
    )
    phone_number = PhoneNumberField().formfield(
        label=_("Phone number"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("Phone number"),
                "id": "form-phone_number",
            },
        ),
    )
    country = CountryField(blank_label=_("Select country"),).formfield(
        label=_("Country"),
        widget=CountrySelectWidget(
            attrs={"class": "form-select form-control mb3", "id": "form-country", "src": ""},
        ),
    )
    state = forms.CharField(
        label=_("Province / State"),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("Province / State"),
                "id": "form-state",
            },
        ),
    )
    city = forms.CharField(
        label=_("City"),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("City"),
                "id": "form-city",
            },
        ),
    )
    postcode = forms.CharField(
        label=_("Postal code"),
        max_length=12,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("Postal code"),
                "id": "form-postcode",
            },
        ),
    )
    address_line_1 = forms.CharField(
        label=_("Address (line 1)"),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("Address (line 1)"),
                "id": "form-address1",
            },
        ),
    )
    address_line_2 = forms.CharField(
        label=_("Address (line 2)"),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("Address (line 2)"),
                "id": "form-address2",
            },
        ),
    )
    delivery_instructions = forms.CharField(
        label=_("Delivery instructions"),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb3",
                "placeholder": _("Delivery instructions"),
                "id": "form-delivery_instructions",
            },
        ),
    )
    
    class Meta:
        model = Address
        fields = (
            "full_name",
            "phone_number",
            "country",
            "state",
            "city",
            "postcode",
            "address_line_1",
            "address_line_2",
            "delivery_instructions",
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].required = True
        self.fields["phone_number"].required = True
        self.fields["country"].required = True
        self.fields["state"].required = True
        self.fields["city"].required = True
        self.fields["postcode"].required = True
        self.fields["address_line_1"].required = True
        self.fields["address_line_2"].required = False
        self.fields["delivery_instructions"].required = False


class AccountDeleteForm(UserLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
