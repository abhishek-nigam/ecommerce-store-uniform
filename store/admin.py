from django.contrib import admin

from .models import *

admin.site.register(School)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductInstance)
admin.site.register(Order)
admin.site.register(OrderItem)