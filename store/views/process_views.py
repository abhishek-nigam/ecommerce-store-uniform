from django.conf import settings

from ..models import ProductInstance

def process_get_amounts(request):
    base_amount = 0
    payable_amount = 0
    additional_charges = 0

    for item in request.session['user_cart'].keys():
        product_instance = ProductInstance.objects.get(instance_id=item)
        item_price =  request.session['user_cart'][item] * float(product_instance.price)
        base_amount = base_amount + item_price

    payable_amount = (100.0/(100.0 - settings.ADDITIONAL_CHARGES_PERCENTAGE)) * float(base_amount)
    additional_charges = payable_amount - base_amount

    base_amount = float("{0:.2f}".format(base_amount))
    additional_charges = float("{0:.2f}".format(additional_charges))
    payable_amount = float("{0:.2f}".format(payable_amount))
    
    return (base_amount, additional_charges, payable_amount)