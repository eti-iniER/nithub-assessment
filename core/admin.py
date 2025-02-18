from django.contrib import admin
from core.models import User, Product, Order, OrderItem

# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
