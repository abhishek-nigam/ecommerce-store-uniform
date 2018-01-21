from django import forms

from ..models import ProductInstance

class ProductInstanceForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = '__all__'