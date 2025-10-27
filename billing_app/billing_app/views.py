from django.shortcuts import render
from masters.models import Company, Customer, Item
from transactions.models import Invoice

def dashboard(request):
    # Choose the correct field for ordering
    # Check which field your Invoice model actually has
    order_field = "-created_at"  # or "-date" if that exists

    invoices = Invoice.objects.all().order_by(order_field)[:5]

    context = {
        "company_count": Company.objects.count(),
        "customer_count": Customer.objects.count(),
        "item_count": Item.objects.count(),
        "invoice_count": Invoice.objects.count(),
        "recent_invoices": invoices,
    }

    return render(request, "dashboard.html", context)
