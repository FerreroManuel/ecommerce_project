from django.contrib import admin

from .models import Address, Customer, WarehouseAddress

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(WarehouseAddress)
