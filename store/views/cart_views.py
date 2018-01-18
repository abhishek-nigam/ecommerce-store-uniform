from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from ..models import ProductInstance
from .process_views import process_get_amounts

def cart_display(request):
    
    cart_items = []
    cart_is_empty = True

    if 'user_cart' in request.session.keys():
        if len(request.session['user_cart'].keys()) == 0:
            cart_is_empty = True
        else:
            for item in request.session['user_cart'].keys():
                item_obj = {}
                cart_is_empty = False

                product_instance = ProductInstance.objects.get(instance_id=item)
                item_obj['product_name'] = product_instance.product.title
                item_obj['instance_size'] = product_instance.size
                item_obj['instance_qty'] = request.session['user_cart'][item]
                item_obj['instance_total_price'] = item_obj['instance_qty'] * float(product_instance.price)
                item_obj['instance_id'] = item

                cart_items.append(item_obj)

            base_amount, additional_charges, payable_amount = process_get_amounts(request)
    else:
        pass


    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'base_amount': base_amount,
        'additional_charges': additional_charges,
        'payable_amount': payable_amount,
        'cart_is_empty': cart_is_empty
    })


def cart_delete_item(request):
    instance_id = request.GET.get('id', False)

    if instance_id:
        if 'user_cart' in request.session.keys():
            if len(request.session['user_cart'].keys()) == 0:
                pass
            else:
                if instance_id in request.session['user_cart'].keys():
                    request.session['user_cart'].pop(instance_id, None)
                    request.session.modified = True    
                else:
                    pass
        else:
            pass
    else:
        pass
    
    return HttpResponseRedirect(reverse('cart-display'))


def cart_add_item(request):

    instance_id = request.GET['id']
    instance_qty = request.GET['qty']

    if 'user_cart' in request.session.keys():
        if instance_id in request.session['user_cart']:
            request.session['user_cart'][instance_id] = request.session['user_cart'][instance_id] + 1
            request.session.modified = True

        else:
            request.session['user_cart'][instance_id] = 1
            request.session.modified = True

    else:
        request.session['user_cart'] = {}
        request.session['user_cart'][instance_id] = 1 # doesn't save session
        request.session.modified = True # saves session explicitly
    
    return HttpResponse("Added to cart")
