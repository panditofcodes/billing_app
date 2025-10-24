from django import forms
from .models import Company, Item, Customer, Address, Contact


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

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["line1", "city", "state", "pincode", "country"]

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["email", "phone"]