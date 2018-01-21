import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..models import Order, ProductInstance


@permission_required('store.can_maintain_orders')
def manage_order_list_new(request):
    order_queryset = Order.objects.filter(is_payed=True, is_fulfilled=False)

    return render(request, 'store/manage/manage_order_list.html', {
        'orders': order_queryset,
        'new': True
    })

@permission_required('store.can_maintain_orders')
def manage_order_list_fulfilled(request):
    order_queryset = Order.objects.filter(is_fulfilled=True)

    return render(request, 'store/manage/manage_order_list.html', {
        'orders': order_queryset,
        'fulfilled': True
    })

@permission_required('store.can_maintain_orders')
def manage_order_list_abandoned(request):
    order_queryset = Order.objects.filter(is_payed=False)

    return render(request, 'store/manage/manage_order_list.html', {
        'orders': order_queryset,
        'abandoned': True
    })

@permission_required('store.can_maintain_orders')
def manage_order_search(request):
    data = {}
    if len(request.GET) == 0:
        data['first_load'] = True

    if request.GET.get("field", False) and request.GET.get("query", False):
        field = request.GET["field"]
        query = request.GET["query"]

        if field in ['order_id', 'customer_name', 'customer_mobile_number', 'fulfilled_by','payment_id']:
            if field == 'order_id':
                order_queryset = Order.objects.filter(order_id=query)
                data['order_id'] = True
            elif field == 'customer_name':
                order_queryset = Order.objects.filter(customer_name=query)
                data['customer_name'] = True
            elif field == 'customer_mobile_number':
                order_queryset = Order.objects.filter(customer_mobile_number=query)
                data['customer_mobile_number'] = True
            elif field == 'payment_id':
                order_queryset = Order.objects.filter(payment_id=query)
                data['payment_id'] = True
            else:
                order_queryset = Order.objects.filter(fulfilled_by=query)
                data['fulfilled_by'] = True

            data['query'] = query
            data['orders'] = order_queryset
        else:
            data['error'] = "Improper request"

    else:
        data['error'] = "Improper request"

    return render(request, 'store/manage/manage_order_search.html', data)

@permission_required('store.can_maintain_orders')
def manage_order_detail(request, pk):
    order_object = get_object_or_404(Order, order_id=pk)
    order_items_products = []

    for order_item in order_object.orderitem_set.all():
        order_dict = {}
        
        order_dict['order_item_id'] = order_item.order_item_id
        order_dict['order_item_qty'] = order_item.quantity

        try:
            product_instance = ProductInstance.objects.get(instance_id=order_item.product_instance_id)
            order_dict['product_name'] = product_instance.product.title
            order_dict['product_instance_id'] = product_instance.instance_id
        
        except:
            order_dict['product_name'] = "Product Instance Deleted"
            order_dict['product_instance_id'] = 0

        order_items_products.append(order_dict)
        
    return render(request, 'store/manage/manage_order_detail.html', {
        'order': order_object,
        'order_items_products': order_items_products
    })


@permission_required('store.can_maintain_orders')
def manage_order_fulfill(request, pk):
    order_object = get_object_or_404(Order, order_id=pk)
    
    order_object.is_fulfilled = True
    order_object.fulfilled_by = request.user.username
    order_object.fulfillment_timestamp = datetime.datetime.now()
    order_object.save()

    return HttpResponseRedirect(reverse('manage-order-detail', args=[order_object.order_id]))