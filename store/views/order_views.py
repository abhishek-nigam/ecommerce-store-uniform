import random, string

from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from .process_views import process_get_amounts
from ..forms import CheckoutForm
from ..models import ProductInstance, Order, OrderItem

import razorpay

def order_checkout_start(request):
    if 'user_cart' in request.session.keys() and len(request.session['user_cart'].keys()) != 0:
        
        if request.method == 'GET':
            base_amount, additional_charges, payable_amount = process_get_amounts(request)
            form = CheckoutForm()
            cart_items = request.session['user_cart']

            cart_items_info = []
            for item in cart_items:
                cart_item_obj = {}
                product_instance = ProductInstance.objects.get(instance_id=item)
                cart_item_obj['product_name'] = product_instance.product.title
                cart_item_obj['product_size'] = product_instance.size
                cart_item_obj['instance_qty'] = cart_items[item]
                cart_item_obj['instance_total_price'] = cart_items[item] * float(product_instance.price)

                cart_items_info.append(cart_item_obj)

            # Passing amounts, and items only to display
            # Will retake the latest data in session before making payment
            return render(request, 'store/checkout_start.html', {
                'base_amount': base_amount,
                'additional_charges': additional_charges,
                'payable_amount': payable_amount,
                'cart_items_info': cart_items_info,
                'form': form # Actually used in submission
            });

        elif request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid():
                customer_name = form.cleaned_data['customer_name']
                customer_phone_no = form.cleaned_data['customer_phone_no']
                customer_address = form.cleaned_data['customer_address']
                
                # Save sessions
                request.session['customer_name'] = customer_name
                request.session['customer_phone_no'] = customer_phone_no
                request.session['customer_address'] = customer_address

                return HttpResponseRedirect(reverse('checkout-confirm-1'))

        else:
            raise Http404

    else:
        raise Http404


def order_checkout_confirm_1(request):
    if ('user_cart' in request.session.keys() and len(request.session['user_cart'].keys()) != 0) and 'customer_name' in request.session.keys() and 'customer_phone_no' in request.session.keys() and 'customer_address' in request.session.keys():
        
        base_amount, additional_charges, payable_amount = process_get_amounts(request)

        cart_items = request.session['user_cart']
        customer_name = request.session['customer_name']
        customer_phone_no = request.session['customer_phone_no']
        customer_address = request.session['customer_address']

        cart_items_info = []
        for item in cart_items:
            cart_item_obj = {}
            product_instance = ProductInstance.objects.get(instance_id=item)
            cart_item_obj['product_name'] = product_instance.product.title
            cart_item_obj['product_size'] = product_instance.size
            cart_item_obj['instance_qty'] = cart_items[item]
            cart_item_obj['instance_total_price'] = cart_items[item] * float(product_instance.price)

            cart_items_info.append(cart_item_obj)

        request.session['confirmed_data'] = True

        return render(request, 'store/checkout_confirm.html', {
            'base_amount': base_amount,
            'additional_charges': additional_charges,
            'payable_amount': payable_amount,
            'cart_items_info' : cart_items_info,
            'customer_name': customer_name,
            'customer_phone_no': customer_phone_no,
            'customer_address': customer_address,
        });

    else:
        raise Http404


def order_checkout_confirm_2(request):
    
    if ('user_cart' in request.session.keys() and len(request.session['user_cart'].keys()) != 0) and 'customer_name' in request.session.keys() and 'customer_phone_no' in request.session.keys() and 'customer_address' in request.session.keys() and ('confirmed_data' in request.session.keys() and request.session['confirmed_data'] == True):

        # Generate random string
        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        # Get amounts
        base_amount, additional_charges, payable_amount = process_get_amounts(request)
        # Customer details
        customer_name = request.session['customer_name']
        customer_phone_no = request.session['customer_phone_no']
        customer_address = request.session['customer_address']


        ## Make order
        order = Order(order_access_token=random_string, base_amount=base_amount, total_amount=payable_amount, customer_name=customer_name, customer_mobile_number=customer_phone_no, customer_address=customer_address)
        order.save() # save explicitly


        # Add all order items to it
        cart_items = request.session['user_cart']
        for item in cart_items:
            product_instance = ProductInstance.objects.get(instance_id=item)

            order_item = OrderItem(order=order, product_instance_id= product_instance.instance_id, quantity=cart_items[item])
            order_item.save() # save explicitly

        
        order_id = order.order_id
        payable_amount_paise = payable_amount * 100

        razorpay_key_id = settings.RAZORPAY_KED_ID

        return render(request, 'store/checkout_pay.html', {
            'order_id': order_id,
            'payable_amount_paise': payable_amount_paise,
            'razorpay_key_id': razorpay_key_id,

            # Some additional info
            'customer_name': customer_name,
            'customer_phone_no': customer_phone_no,
            'customer_address': customer_address
        })
    
    else:
        raise Http404


def order_checkout_end(request):

    if request.method == 'POST' and request.POST.get('correct_submit', None) and request.POST.get('razorpay_payment_id', None):

        # Initially clear session data
        request.session.clear()        
        
        # collect payment id from automaitc form submit
        payment_id = request.POST.get('razorpay_payment_id', None)

        # get client
        client = razorpay.Client(auth=(settings.RAZORPAY_KED_ID, settings.RAZORPAY_KEY_SECRET))
        # get payment object
        resp_get_payment = client.payment.fetch(payment_id)

        # check that payment was authorized
        if resp_get_payment["status"] == "authorized":

            paid_amount = resp_get_payment["amount"]
            # description = resp_get_payment["description"]
            # contact_no = resp_get_payment["contact"]
            # total_charges = resp_get_payment["fee"]
            # tax_charges = resp_get_payment["tax"]
            # created_time = resp_get_payment["created_at"]
            # address = resp_get_payment["notes"]['address']
            order_id_str = resp_get_payment["notes"]['dborderid']

            order_id = int(order_id_str)

            order = Order.objects.get(order_id=order_id)

            if float(order.total_amount)*100 == paid_amount:
                
                if order.is_payed == False:

                    order.is_payed = True
                    order.payment_id = payment_id
                    order.save() # explicitly save

                    # capture payment
                    resp_capture_payment = client.payment.capture(payment_id, paid_amount)

                    if resp_capture_payment["status"] == "captured":
                        
                        order.is_captured = True
                        order.save() # explicitly save

                        return render(request, 'store/checkout_end.html', {
                            'order_id': order_id,
                            'order_access_token': order.order_access_token,
                            'order_success': True
                        })

                    else:
                        print("Problem in capturing payment")
                        return render(request, 'store/checkout_end.html', {
                            'order_failure': True
                        })

                else:
                    print("Order is already payed")
                    return render(request, 'store/checkout_end.html', {
                        'order_failure': True
                    })

            else:
                print("Payment amount mismatched")
                return render(request, 'store/checkout_end.html', {
                    'order_failure': True
                })

        else:
            print("Payment was not authorised")
            return render(request, 'store/checkout_end.html', {
                'order_failure': True
            })

    else:
        raise Http404