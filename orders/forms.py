from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from .models import Order




class OrderForm(forms.ModelForm):
    full_name = forms.CharField(
        label='Nombre completo',
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Nombre completo',
                'id': 'form-fullname',
            }
        )
    )
    address1 = forms.CharField(
        label='Domicilio (línea 1)',
        min_length=4,
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Domicilio (línea 1)',
                'id': 'form-address1',
            }
        )
    )
    address2 = forms.CharField(
        label='Domicilio (línea 2)',
        min_length=4,
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Domicilio (línea 2)',
                'id': 'form-address2',
            }
        )
    )
    city = forms.CharField(
        label='Ciudad',
        min_length=4,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Ciudad',
                'id': 'form-city',
                'readonly': 'readonly',         # Sólo envíos a Rosario x el momento (cambiar views si se activa)
            }
        )
    )
    phone = PhoneNumberField().formfield(
        label='Teléfono',
        min_length=4,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Teléfono',
                'id': 'form-phone',
            }
        )
    )
    postcode = forms.CharField(
        label='Código postal',
        min_length=4,
        max_length=12,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Código postal',
                'id': 'form-postcode',
            }
        )
    )
    total_paid = forms.DecimalField(
        label='Total a abonar',
        max_digits=20,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Total a abonar',
                'id': 'form-totalpaid',
                'readonly': 'readonly',
            }
        )
    )
    order_key = forms.CharField(
        label='Nro. de recibo/transferencia',
        min_length=4,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Nro. recibo/transferencia',
                'id': 'form-orderkey',
                'readonly': 'readonly',
            }
        )
    )
    billing_status = forms.BooleanField(
        label='Pago',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'form-billingstatus',
                'disabled': True,
            }
        )
    )

    class Meta:
        model = Order
        fields = (
        'full_name',
        'address1',
        'address2',
        'city',
        'phone',
        'postcode',
        'total_paid',
        'order_key',
        'billing_status',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].required = True
        self.fields['address1'].required = True
        self.fields['address2'].required = False
        self.fields['city'].required = True
        self.fields['phone'].required = True
        self.fields['postcode'].required = True
        self.fields['total_paid'].required = True
        self.fields['order_key'].required = False
