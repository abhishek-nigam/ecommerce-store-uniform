from django import forms

class CheckoutForm(forms.Form):
    customer_name = forms.CharField(label="Name", max_length=255, required=True)
    customer_phone_no = forms.IntegerField(label="Contact No",required=True, help_text="eg. 9810010090")
    customer_address = forms.CharField(label="Delivery Address", required=True) # TODO: split address into multiple fields

    #TODO: Do some validation here