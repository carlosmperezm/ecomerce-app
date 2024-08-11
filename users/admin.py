""" This file is used to register the models in the admin panel. """

from django.contrib import admin

from users.models import User, Address

admin.site.register(User)
admin.site.register(Address)
