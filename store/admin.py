from django.contrib import admin
from .models import Category,Product,Order,OrderProduct,CartItem, Profile

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(CartItem)
admin.site.register(Profile)
