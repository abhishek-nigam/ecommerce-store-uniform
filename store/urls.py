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

    url(r'^manage/school/list/$', manage_school_list, name="manage-school-list"),
    url(r'^manage/school/add/$', manage_school_add, name="manage-school-add"),
    url(r'^manage/school/(?P<pk>\d+)/update/$', manage_school_update, name="manage-school-update"),
    url(r'^manage/school/(?P<pk>\d+)/delete/$', manage_school_delete, name="manage-school-delete"),

    url(r'^manage/category/list/$', manage_category_list, name="manage-category-list"),
    url(r'^manage/category/add/$', manage_category_add, name="manage-category-add"),
    url(r'^manage/category/(?P<pk>\d+)/update/$', manage_category_update, name="manage-category-update"),
    url(r'^manage/category/(?P<pk>\d+)/delete/$', manage_category_delete, name="manage-category-delete"),

    url(r'^manage/product/list/$', manage_product_list, name="manage-product-list"),
    url(r'^manage/product/add/$', manage_product_add, name="manage-product-add"),
    url(r'^manage/product/(?P<pk>\d+)/update/$', manage_product_update, name="manage-product-update"),
    url(r'^manage/product/(?P<pk>\d+)/delete/$', manage_product_delete, name="manage-product-delete"),

    url(r'^manage/instance/list/$', manage_product_instance_list, name="manage-product-instance-list"),
    url(r'^manage/instance/add/$', manage_product_instance_add, name="manage-product-instance-add"),
    url(r'^manage/instance/(?P<pk>\d+)/update/$', manage_product_instance_update, name="manage-product-instance-update"),
    url(r'^manage/instance/(?P<pk>\d+)/delete/$', manage_product_instance_delete, name="manage-product-instance-delete"),

    url(r'^manage/order/(?P<pk>\d+)/$', manage_order_detail, name="manage-order-detail"),
    url(r'^manage/order/(?P<pk>\d+)/fulfill/$', manage_order_fulfill, name="manage-order-fulfill"),
    url(r'^manage/order/list/new/$', manage_order_list_new, name="manage-order-list-new"),
    url(r'^manage/order/list/fulfilled/$', manage_order_list_fulfilled, name="manage-order-list-fulfilled"),
    url(r'^manage/order/list/abandoned/$', manage_order_list_abandoned, name="manage-order-list-abandoned"),
    url(r'^manage/order/search/$', manage_order_search, name="manage-order-search"),
]