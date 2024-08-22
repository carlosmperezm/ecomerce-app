from django.contrib import admin

from shopping_and_payments.models import CartItem, ShoppingCart, ShopOrder, OrderStatus

admin.site.register(CartItem)
admin.site.register(ShoppingCart)
admin.site.register(ShopOrder)
admin.site.register(OrderStatus)

