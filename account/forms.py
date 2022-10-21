from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.modelfields import PhoneNumberField
from .models import UserBase


class RegistrationForm(forms.ModelForm):

    user_name = forms.CharField(
        label='Nombre de usuario',
        min_length=4,
        max_length=50,
        help_text='*',
        error_messages={
            'required': 'El campo Nombre de usuario es obligatorio',
        },
    )
    email = forms.EmailField(
        max_length=100,
        help_text='*',
        error_messages={
            'required': 'El campo Email es obligatorio',
        },
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'El campo Contraseña es obligatorio',
        },
    )
    password2 = forms.CharField(
        label='Repita la contraseña',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'El campo Contraseña es obligatorio',
        },
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {
                'class': 'form-control mb3',
                'placeholder': 'Nombre de usuario',
                'name': 'user_name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'class': 'form-control mb3',
                'placeholder': 'Email',
                'name': 'email',
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control mb3',
                'placeholder': 'Contraseña',
                'name': 'password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Repita contraseña',
                'name': 'password2',
            }
        )


    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("El nombre de usuario ya existe")
        return user_name


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cd['password2']


    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ingresado ya se encuentra registrado')
        return email


    class Meta:
        model = UserBase
        fields = ('user_name', 'email')


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Nombre de usuario',
                'id': 'login-username',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Contraseña',
                'id': 'login-pwd',
            }
        )
    )


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Email',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Email',
                'id': 'form-email',
                'readonly': 'readonly',
            },
        ),
    )
    user_name = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Nombre de usuario',
                'id': 'form-username',
                'readonly': 'readonly',
            },
        ),
    )
    first_name = forms.CharField(
        label='Nombre',
        min_length=4,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Nombre',
                'id': 'form-firstname',
            },
        ),
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Apellido',
                'id': 'form-lastname',
            },
        ),
    )
    country = CountryField(blank_label='Seleccione un país',).formfield(
        label='País',
        widget=CountrySelectWidget(
            attrs={
                'class': 'form-select form-control mb3',
                'id': 'form-country',
                'src': ''
            },
        ),
    )
    state = forms.CharField(
        label='Provincia / Estado',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Provincia / Estado',
                'id': 'form-state',
            },
        ),
    )
    city = forms.CharField(
        label='Ciudad',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Ciudad',
                'id': 'form-city',
            },
        ),
    )
    postcode = forms.CharField(
        label='Código postal',
        max_length=12,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Código postal',
                'id': 'form-postcode',
            },
        ),
    )
    address_line_1 = forms.CharField(
        label='Domicilio (línea 1)',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Domicilio (línea 1)',
                'id': 'form-address1',
            },
        ),
    )
    address_line_2 = forms.CharField(
        label='Domicilio (línea 2)',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Domicilio (línea 2)',
                'id': 'form-address2',
            },
        ),
    )
    cell_phone = PhoneNumberField().formfield(
        label='Teléfono celular',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Teléfono celular',
                'id': 'form-cellphone',
            },
        ),
    )
    home_phone = PhoneNumberField().formfield(
        label='Teléfono fijo',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb3',
                'placeholder': 'Teléfono fijo',
                'id': 'form-homephone',
            },
        ),
    )


    class Meta:
        model = UserBase
        fields = (
            'email',
            'user_name',
            'first_name',
            'last_name',
            'country',
            'state',
            'city',
            'postcode',
            'address_line_1',
            'address_line_2',
            'cell_phone',
            'home_phone',
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['country'].required = False
        self.fields['state'].required = False
        self.fields['city'].required = False
        self.fields['postcode'].required = False
        self.fields['address_line_1'].required = False
        self.fields['address_line_2'].required = False
        self.fields['cell_phone'].required = False
        self.fields['home_phone'].required = False


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Email',
                'id': 'form-email'
            }
        )
    )


    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError('La dirección de correo electrónico idicada no se encuentra registrada')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Nueva contraseña',
                'id': 'form-newpass1'
            }
        )
    )
    new_password2 = forms.CharField(
        label='Repita contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Repita contraseña',
                'id': 'form-newpass2'
            }
        )
    )
