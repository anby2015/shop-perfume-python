from django.contrib import admin
from Shop.models import Category, Product

class Admin:
    admin.site.register(Category)
    admin.site.register(Product)