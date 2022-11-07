from django.urls import path

from . import views

app_name = 'orders'


urlpatterns = [
    path('order/', views.order, name='order'),
    path('order/add/', views.add, name='add'),
]
