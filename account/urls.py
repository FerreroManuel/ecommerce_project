from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm

app_name = 'account'


urlpatterns = [
    # User registration
    path(                       # register
        'register/',
        views.account_register,
        name='register',
    ),
    path(                       # login
        'login/',
        LoginView.as_view(
            template_name='account/login.html',
            form_class=UserLoginForm,
            next_page='/',
        ),
        name='login',
    ),
    path(                       # logout
        'logout/',
        LogoutView.as_view(next_page='/account/login/'),
        name='logout',
    ),
    path(                       # activate
        'activate/<slug:uidb64>/<slug:token>/',
        views.account_activate,
        name='activate',
    ),

    # Password reset
    path(                       # pwdreset
        'password_reset/',
        PasswordResetView.as_view(
            template_name='account/password_reset/password_reset_form.html',
            success_url='password_reset_email_confirm',
            email_template_name='account/password_reset/password_reset_email.html',
            form_class=PwdResetForm,
        ),
        name='pwdreset',
    ),
    path(                       # password_reset_confirm
        'password_reset_confirm/<uidb64>/<token>',
        PasswordResetConfirmView.as_view(
            template_name='account/password_reset/password_reset_confirm.html',
            success_url='/account/password_reset_complete/',
            form_class=PwdResetConfirmForm,
        ),
        name='password_reset_confirm',
    ),
    path(                       # password_reset_done
        'password_reset/password_reset_email_confirm/',
        TemplateView.as_view(template_name='account/password_reset/reset_status.html'),
        name='password_reset_done',
    ),
    path(                       # password_reset_complete
        'password_reset_complete/',
        TemplateView.as_view(template_name='account/password_reset/reset_status.html'),
        name='password_reset_complete',
    ),

    # User dashboard
    path(                       # dashboard
        'dashboard/',
        views.dashboard,
        name='dashboard',
    ),
    path(                       # edit_details
        'profile/edit/',
        views.edit_details,
        name='edit_details',
    ),
    path(                       # delete_user
        'profile/delete_user/',
        views.delete_user,
        name='delete_user',
    ),
    path(                       # delete_confirm
        'profile/delete_confirm/',
        TemplateView.as_view(template_name='account/dashboard/delete_confirm.html'),
        name='delete_confirm',
    ),
    
    # Addresses
    path(                       # addresses
        "addresses/",
        views.view_address,
        name="addresses",
    ),
    path(                       # add_address
        "add_address/",
        views.add_address,
        name="add_address",
    ),
    path(                       # edit_address
        "addresses/edit/<slug:id>/",
        views.edit_address,
        name="edit_address",
    ),
    path(                       # delete_address
        "addresses/delete/<slug:id>/",
        views.delete_address,
        name="delete_address",
    ),
    path(                       # set_default
        "addresses/set_default/<slug:id>/",
        views.set_default,
        name="set_default",
    ),
]
