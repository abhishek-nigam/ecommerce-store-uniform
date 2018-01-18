from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from .process_views import process_get_amounts
from ..forms import CheckoutForm

def order_checkout_start(request):
    if 'user_cart' in request.session.keys() and len(request.session['user_cart'].keys()) != 0:
        
        if request.method == 'GET':
            base_amount, additional_charges, payable_amount = process_get_amounts(request)
            form = CheckoutForm()
            cart_items = request.session['user_cart']

            # Passing amounts, and items only to display
            # Will retake the latest data in session before making payment
            return render(request, 'store/checkout_start.html', {
                'base_amount': base_amount,
                'additional_charges': additional_charges,
                'payable_amount': payable_amount,
                'cart_items': cart_items,
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

                return HttpResponseRedirect(reverse('checkout-confirm'))

        else:
            raise Http404

    else:
        raise Http404


def order_checkout_confirm(request):
    if ('user_cart' in request.session.keys() and len(request.session['user_cart'].keys()) != 0) and 'customer_name' in request.session.keys() and 'customer_phone_no' in request.session.keys() and 'customer_address' in request.session.keys():
        
        base_amount, additional_charges, payable_amount = process_get_amounts(request)
        cart_items = request.session['user_cart']
        customer_name = request.session['customer_name']
        customer_phone_no = request.session['customer_phone_no']
        customer_address = request.session['customer_address']
        razorpay_key_id = settings.RAZORPAY_KED_ID

        return(request, 'store/checkout_confirm.html', {
            'base_amount': base_amount,
            'additional_charges': additional_charges,
            'payable_amount': payable_amount,
            'cart_items': cart_items,
            'customer_name': customer_name,
            'customer_phone_no': customer_phone_no,
            'customer_address': customer_address,
            'razorpay_key_id': razorpay_key_id
        });

    else:
        raise Http404