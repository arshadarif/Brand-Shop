from django.contrib import admin
from django.urls import path,re_path
from . import views

app_name = 'store'

urlpatterns = [
    path('',views.index,name='index'),
    path('contact_us/',views.contact,name='contact_us'),
    path('privacy_policy/',views.privacy_policy,name='privacy_policy'),
    path('about_us/',views.about_us,name='about_us'),
    re_path(r'^product/(?P<ID>\w+)',views.product,name='product'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('wishlist/',views.user_wishlist,name='wishlist'),
    path('add_tocart/',views.add_cart,name='add_cart'),
    path('change_qty/',views.change_qty,name='change_qty'),
    path('add_wishlist',views.add_wishlist,name='add_wishlist'),
    path('remove_wishlist',views.remove_wishlist,name='remove_wishlist'),
    path('remove_cart',views.remove_cart,name='remove_cart'),
    path('search_ajax/',views.search_ajax,name='search_ajax'),
    path('search/',views.search,name='search'),
]