from django import forms
from .models import Company, Item, Customer, Address, Contact


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "hsn_code", "price", "gst_rate", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "hsn_code": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "gst_rate": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["line1", "city", "state", "pincode", "country"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["email", "phone"]
