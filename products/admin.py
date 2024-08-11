""" This file is used to register the models in the admin panel. """

from django.contrib import admin

from products.models import Product, Category

admin.site.register(Product)
admin.site.register(Category)
