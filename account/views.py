from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from orders.views import user_orders
from store.models import Product

from .forms import AccountDeleteForm, RegistrationForm, UserAddressForm, UserEditForm
from .models import Address, Customer
from .tokens import account_activation_token


def account_register(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()

            # Setup confirmation email
            current_site = get_current_site(request)
            subject = "Activación de cuenta | BookStore"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, "account/registration/register_valid.html")
    else:
        registerForm = RegistrationForm()

    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except:
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


@login_required(login_url=reverse_lazy("account:login"))
def dashboard(request):
    return render(request, "account/dashboard/dashboard.html")


@login_required(login_url=reverse_lazy("account:login"))
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, "account/edit/edit_details.html", {"user_form": user_form})


@login_required
def delete_confirmation(request):
    if request.method == "POST":
        delete_form = AccountDeleteForm(data=request.POST)
    else:
        delete_form = AccountDeleteForm()
    return render(request, "account/edit/delete_confirmation.html", {'delete_form': delete_form})


@login_required
def delete_user(request):
    if request.method == "POST":
        print(request.POST["username"])
        delete_form = AccountDeleteForm(data=request.POST)
        if delete_form.is_valid() and request.POST["username"] == request.user.email:
            user = Customer.objects.get(email=request.user.email)
            user.is_active = False
            user.save()
            logout(request)
            return redirect("account:delete_confirmed")
        else:
            messages.error(request, "Email o contaseñas incorrectos")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def pwd_change_confirm(request):
    messages.success(request, "Contraseña modificada exitosamente.")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# -------- ADDRESSES --------

@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form = address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/edit/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/edit/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    address = Address.objects.get(pk=id, customer=request.user)
    if address.default:
        Address.objects.filter(pk=id, customer=request.user).update(default=False)
    else:
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect("account:addresses")


# --------- ORDERS ---------

@login_required
def orders(request):
    orders, orders_paid = user_orders(request)
    return render(request, "account/dashboard/orders.html", {"orders": orders, "orders_paid": orders_paid})




# -------- WISHLIST --------

@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/dashboard/user_wishlist.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, f"Se eliminó <b>'{product.title}'</b> de tu lista de favoritos")
    else:
        messages.success(request, f"Se agregó <b>'{product.title}'</b> a tu lista de favoritos")
        product.users_wishlist.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
