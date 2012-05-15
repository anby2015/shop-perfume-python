from django import forms

class ProductDetailForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, required=True)