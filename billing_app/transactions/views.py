# views.py (transactions app)
import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db import transaction

from .models import Invoice, InvoiceItem
from masters.models import Customer, Company, Item
from .forms import InvoiceForm


@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()

    for inv in invoices:
        inv.get_edit_url = reverse("invoice_edit", args=[inv.id])
        inv.get_delete_url = reverse("invoice_delete", args=[inv.id])
        inv.customer_name = inv.customer.name if inv.customer else "—"
        total_amount = sum(item.total for item in inv.items.all()) if hasattr(inv, "items") else 0
        inv.total_amount_display = f"₹{total_amount:.2f}"

    columns = [
        {"label": "Invoice No", "attr": "invoice_number", "clickable": True, "width": "15%"},
        {"label": "Date", "attr": "date", "clickable": False, "width": "15%"},
        {"label": "Customer", "attr": "customer_name", "clickable": False, "width": "25%"},
        {"label": "Total Amount", "attr": "total_amount_display", "clickable": False, "width": "20%"},
        {"label": "Status", "attr": "status", "clickable": False, "width": "15%"},
        {"label": "Actions", "attr": "custom_actions", "clickable": False, "width": "10%"},
    ]

    context = {
        "object_list": invoices,
        "columns": columns,
        "add_url": reverse("invoice_create"),
        "list_title": "Invoice List",
        "object_name": "Invoice",
        "list_icon": "bi bi-receipt-cutoff",
    }

    return render(request, "transactions/invoice/invoice_list.html", context)


@login_required
def invoice_create(request):
    customers = Customer.objects.all()
    companies = Company.objects.all()
    items = Item.objects.all()

    if request.method == "POST":
        company_id = request.POST.get("company")
        customer_id = request.POST.get("customer")
        invoice_no = request.POST.get("invoice_no")

        item_ids = request.POST.getlist("item")
        quantities = request.POST.getlist("quantity")

        subtotal = Decimal("0")
        gst_total = Decimal("0")

        # Calculate totals first
        for i, item_id in enumerate(item_ids):
            if not item_id:
                continue
            item_obj = Item.objects.get(id=item_id)
            qty = Decimal(quantities[i] or 0)
            line_total = item_obj.price * qty
            gst = (line_total * item_obj.gst_rate) / Decimal("100")
            subtotal += line_total
            gst_total += gst

        # Create invoice header
        invoice = Invoice.objects.create(
            invoice_number=invoice_no,
            company_id=company_id,
            customer_id=customer_id,
            subtotal=subtotal,
            gst_total=gst_total,
            grand_total=subtotal + gst_total,
        )

        # Create invoice items
        for i, item_id in enumerate(item_ids):
            if not item_id:
                continue
            item_obj = Item.objects.get(id=item_id)
            qty = Decimal(quantities[i] or 0)
            line_total = item_obj.price * qty
            gst = (line_total * item_obj.gst_rate) / Decimal("100")
            InvoiceItem.objects.create(
                invoice=invoice,
                item=item_obj,
                quantity=qty,
                price=item_obj.price,
                gst_rate=item_obj.gst_rate,
                total=line_total + gst,
            )

        return redirect("invoice_detail", invoice.id)

    context = {
        "customers": customers,
        "companies": companies,
        "items": items,
        "form_title": "Create Invoice",
        "list_url": reverse("invoice_list"),
        "invoice": None,
        "line_items_json": mark_safe("[]"),
    }

    return render(request, "transactions/invoice/invoice_form.html", context)


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.items.all()

    context = {
        "invoice": invoice,
        "items": items,
        "object": invoice,
        "title": f"Invoice #{invoice.invoice_number}",
        "object_name": "Invoice",
        "edit_url": reverse("invoice_edit", args=[invoice.id]),
        "delete_url": reverse("invoice_delete", args=[invoice.id]),
        "add_url": reverse("invoice_create"),
        "back_url": reverse("invoice_list"),
    }

    return render(request, "transactions/invoice/invoice_detail.html", context)


@login_required
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    customers = Customer.objects.all()
    companies = Company.objects.all()
    items = Item.objects.all()

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            # Use transaction so header + lines update atomically
            with transaction.atomic():
                invoice = form.save()

                # get posted parallel arrays
                posted_line_ids = request.POST.getlist("line_id")      # '' or existing id
                posted_item_ids = request.POST.getlist("item")
                posted_qtys = request.POST.getlist("quantity")

                kept_line_ids = []
                subtotal = Decimal("0")
                gst_total = Decimal("0")

                # iterate over posted rows by index
                for idx, item_id in enumerate(posted_item_ids):
                    if not item_id:
                        continue
                    qty = Decimal(posted_qtys[idx] or 0)
                    item_obj = Item.objects.get(pk=item_id)
                    line_total = item_obj.price * qty
                    gst = (line_total * item_obj.gst_rate) / Decimal("100")

                    # check if existing line_id present
                    line_id = posted_line_ids[idx] if idx < len(posted_line_ids) else ''
                    if line_id:
                        try:
                            line = InvoiceItem.objects.get(pk=line_id, invoice=invoice)
                            # update existing
                            line.item = item_obj
                            line.quantity = qty
                            line.price = item_obj.price
                            line.gst_rate = item_obj.gst_rate
                            line.total = line_total + gst
                            line.save()
                            kept_line_ids.append(line.id)
                        except InvoiceItem.DoesNotExist:
                            # fallback: create new
                            new_line = InvoiceItem.objects.create(
                                invoice=invoice,
                                item=item_obj,
                                quantity=qty,
                                price=item_obj.price,
                                gst_rate=item_obj.gst_rate,
                                total=line_total + gst,
                            )
                            kept_line_ids.append(new_line.id)
                    else:
                        # new line
                        new_line = InvoiceItem.objects.create(
                            invoice=invoice,
                            item=item_obj,
                            quantity=qty,
                            price=item_obj.price,
                            gst_rate=item_obj.gst_rate,
                            total=line_total + gst,
                        )
                        kept_line_ids.append(new_line.id)

                    subtotal += line_total
                    gst_total += gst

                # delete any lines removed in the UI
                invoice.items.exclude(id__in=kept_line_ids).delete()

                # update invoice totals
                invoice.subtotal = subtotal
                invoice.gst_total = gst_total
                invoice.grand_total = subtotal + gst_total
                invoice.save()

            return redirect("invoice_detail", pk=invoice.id)
        # if form invalid, fall through to re-render template with form & errors

    # GET (or re-render after invalid POST) build JSON for JS
    lines = []
    for line in invoice.items.all():
        lines.append({
            "line_id": line.id,
            "item_id": line.item.id,
            "qty": float(line.quantity),
            "price": float(line.price),
            "gst": float(getattr(line, "gst_rate", line.item.gst_rate or 0)),
        })

    form = InvoiceForm(instance=invoice)

    context = {
        "form": form,
        "object": invoice,
        "invoice": invoice,
        "title": "Edit Invoice",
        "form_title": "Edit Invoice",
        "list_url": reverse("invoice_list"),
        "add_url": reverse("invoice_create"),
        "customers": customers,
        "companies": companies,
        "items": items,
        "line_items_json": mark_safe(json.dumps(lines)),
    }
    return render(request, "transactions/invoice/invoice_form.html", context)


@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        invoice.delete()
        return redirect("invoice_list")
    return render(
        request,
        "transactions/invoice/invoice_confirm_delete.html",
        {"invoice": invoice, "object_name": "Invoice", "back_url": reverse("invoice_list")},
    )


@login_required
def invoice_print(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.items.all()
    return render(
        request,
        "printformats/invoice_print.html",
        {"invoice": invoice, "items": items},
    )
