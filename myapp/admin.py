from django.contrib import admin
from .models import Client, Product, Order, OrderProduct

admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
