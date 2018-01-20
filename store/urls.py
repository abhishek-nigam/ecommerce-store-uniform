from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^demo/$', demo, name="demo"),

    url(r'^product/list/$', product_list , name="product-list"),
    url(r'^product/(?P<product_id>\d+)/$', product_detail, name="product-detail"),

    url(r'^cart/$', cart_display, name="cart-display"),
    url(r'^cart/add/$', cart_add_item, name="cart-add-item"),
    url(r'^cart/delete/$', cart_delete_item, name="cart-delete-item"),

    url(r'^checkout/start/$', order_checkout_start, name="checkout-start"),
    url(r'^checkout/confirm/$', order_checkout_confirm_1, name="checkout-confirm-1"),
    url(r'^checkout/confirm_details/$', order_checkout_confirm_2, name="checkout-confirm-2"),
    url(r'^checkout/end/$', order_checkout_end, name="checkout-end"),
]