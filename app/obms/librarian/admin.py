from django.contrib import admin

# Register your models here.
from .models import Book, ShoppingCart, Reader

admin.site.register(Book)
admin.site.register(ShoppingCart)
admin.site.register(Reader)