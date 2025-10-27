from django import forms
from .models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["company", "customer", "invoice_number", "date", "due_date", "status"]
        widgets = {
            "company": forms.Select(attrs={"class": "form-control"}),
            "customer": forms.Select(attrs={"class": "form-control"}),
            "invoice_number": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Auto-generate invoice number if creating a new invoice
        if not self.instance.pk:
            last_invoice = Invoice.objects.order_by("id").last()
            if last_invoice and last_invoice.invoice_number:
                try:
                    last_num = int(str(last_invoice.invoice_number).split("-")[-1])
                    new_num = last_num + 1
                except ValueError:
                    new_num = last_invoice.id + 1
            else:
                new_num = 1
            self.fields["invoice_number"].initial = f"INV-{new_num:05d}"
