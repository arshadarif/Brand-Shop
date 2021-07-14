from django.contrib import admin
from.models import (Product,Cart,CartItem,CheckOut,OrderCartItems,OrderCart,
                    WishList,WishListItem)
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CheckOut)
admin.site.register(OrderCart)
admin.site.register(OrderCartItems)
admin.site.register(WishList)
admin.site.register(WishListItem)