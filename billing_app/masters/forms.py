from django import forms
from .models import Company, Item, Customer


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'