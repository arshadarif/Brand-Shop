from django.contrib import admin
from django.urls import path,include,re_path
from . import views

app_name = 'account'

urlpatterns = [
    re_path(r'^$',views.account,name='account'),
    path('orders/',views.orders,name='orders'),
    path('address/',views.address,name='address'),
    path('account_details/',views.ac_details,name='ac_detail'),
    path('adress/edit_address/',views.edit_address,name='edit_address'),
    re_path(r'^orders/track/(?P<ID>\w+)/',views.track,name='track'),
    path('logout/',views.log_out,name='logout'),
    path('forgot_password/',views.forgot_mail,name='forgot_password'),
    re_path(r'^change_password/(?P<ID>\w+)',views.lost_password,name='password_change'),
    re_path(r'^activate/(?P<ID>\w+)',views.activate,name='activate'),
    re_path(r'^return/(?P<ID>\w+)',views.return_item,name='return'),
]