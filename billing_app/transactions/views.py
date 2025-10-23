from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Invoice, InvoiceItem
from masters.models import Customer, Company, Item
from decimal import Decimal


@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, "transactions/invoice_list.html", {"invoices": invoices})


@login_required
def invoice_create(request):
    customers = Customer.objects.all()
    companies = Company.objects.all()
    items = Item.objects.all()

    if request.method == "POST":
        company_id = request.POST["company"]
        customer_id = request.POST["customer"]
        invoice_no = request.POST["invoice_no"]
        item_ids = request.POST.getlist("item")
        quantities = request.POST.getlist("quantity")

        subtotal = Decimal("0")
        gst_total = Decimal("0")

        for i, item_id in enumerate(item_ids):
            item = Item.objects.get(id=item_id)
            qty = Decimal(quantities[i])
            line_total = item.price * qty
            gst = (line_total * item.gst_rate) / 100
            subtotal += line_total
            gst_total += gst

        invoice = Invoice.objects.create(
            invoice_no=invoice_no,
            company_id=company_id,
            customer_id=customer_id,
            subtotal=subtotal,
            gst_total=gst_total,
            grand_total=subtotal + gst_total,
        )

        for i, item_id in enumerate(item_ids):
            item = Item.objects.get(id=item_id)
            qty = Decimal(quantities[i])
            line_total = item.price * qty
            gst = (line_total * item.gst_rate) / 100
            InvoiceItem.objects.create(
                invoice=invoice,
                item=item,
                quantity=qty,
                price=item.price,
                gst_rate=item.gst_rate,
                total=line_total + gst,
            )

        return redirect("invoice_detail", invoice.id)

    return render(
        request,
        "transactions/invoice_form.html",
        {"customers": customers, "companies": companies, "items": items},
    )


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    return render(request, "transactions/invoice_detail.html", {"invoice": invoice})


@login_required
def invoice_print(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    items = invoice.items.all()
    return render(
        request, "printformats/invoice_print.html", {"invoice": invoice, "items": items}
    )


@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        invoice.delete()
        return redirect("invoice_list")
    return render(
        request, "transactions/invoice_confirm_delete.html", {"invoice": invoice}
    )
