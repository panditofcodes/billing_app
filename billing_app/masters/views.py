from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from .models import Company, Item, Customer, Address, Contact
from .forms import CompanyForm, ItemForm, CustomerForm, AddressForm, ContactForm


# ------------------ Company Views ------------------ #
@login_required
def company_list(request):
    companies = Company.objects.all()
    for c in companies:
        c.address_display = f"{c.address.line1}, {c.address.city}" if c.address else ""
        c.contact_display = f"{c.contact.email} / {c.contact.phone}" if c.contact else ""
        c.get_edit_url = reverse("company_edit", args=[c.id])
        c.get_delete_url = reverse("company_delete", args=[c.id])

    columns = [
        {"label": "Name", "attr": "name", "clickable": True, "width": "22%"},
        {"label": "Address", "attr": "address_display", "clickable": False, "width": "25%"},
        {"label": "Contact", "attr": "contact_display", "clickable": False, "width": "25%"},
        {"label": "GSTIN", "attr": "gst_number", "clickable": False, "width": "18%"},
        {"label": "Actions", "attr": "custom_actions", "clickable": False, "width": "10%"},
    ]

    context = {
        "object_list": companies,
        "columns": columns,
        "add_url": reverse("company_create"),
        "list_title": "Company List",
        "object_name": "Company",
        "list_icon": "bi bi-building",
    }
    return render(request, "masters/company/company_list.html", context)



@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)

    context = {
        "company": company,
        "object": company,
        "title": "Company Details",
        "object_name": "Company",
        "edit_url": reverse("company_edit", args=[company.id]),
        "delete_url": reverse("company_delete", args=[company.id]),
        "add_url": reverse("company_create"),
        "back_url": reverse("company_list"),
    }

    return render(request, "masters/company/company_detail.html", context)


@login_required
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("company_list")
    else:
        form = CompanyForm()

    addresses = Address.objects.all()
    contacts = Contact.objects.all()

    context = {
        "form": form,
        "addresses": addresses,
        "contacts": contacts,
        "title": "Add Company",               # ✅ For page title
        "list_url": reverse("company_list"),  # ✅ For Back button
    }

    return render(request, "masters/company/company_form.html", context)

@login_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect("company_list")
    else:
        form = CompanyForm(instance=company)

    context = {
        "form": form,
        "object": company,
        "title": "Edit Company",
        "form_title": "Edit Company",
        "list_url": reverse("company_list"),
        "add_url": reverse("company_create"),
    }

    return render(request, "masters/company/company_form.html", context)



@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        company.delete()
        return redirect("company_list")
    return render(
        request, "masters/company/company_confirm_delete.html", {"company": company}
    )


# ------------------ Address Views ------------------ #
@login_required
def address_create(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("company_create")
    else:
        form = AddressForm()
    return render(request, "masters/address/address_form.html", {"form": form})


# ------------------ Address AJAX ------------------ #
@login_required
def address_create_ajax(request):
    if request.method == "POST":
        line1 = request.POST.get("line1")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        country = request.POST.get("country")
        addr = Address.objects.create(
            line1=line1, city=city, state=state, pincode=pincode, country=country
        )
        return JsonResponse(
            {
                "id": addr.id,
                "line1": addr.line1,
                "city": addr.city,
                "state": addr.state,
                "pincode": addr.pincode,
                "country": addr.country,
            }
        )
    return JsonResponse({"error": "Invalid request"}, status=400)


# ------------------ Contact Views ------------------ #
@login_required
def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("company_create")
    else:
        form = ContactForm()
    return render(request, "masters/contact/contact_form.html", {"form": form})


# ------------------ Contact AJAX ------------------ #
@login_required
def contact_create_ajax(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        contact = Contact.objects.create(email=email, phone=phone)
        return JsonResponse(
            {"id": contact.id, "email": contact.email, "phone": contact.phone}
        )
    return JsonResponse({"error": "Invalid request"}, status=400)


# ------------------ Item Views ------------------ #
@login_required
def item_list(request):
    items = Item.objects.all()

    for i in items:
        i.get_edit_url = reverse("item_edit", args=[i.id])
        i.get_delete_url = reverse("item_delete", args=[i.id])

    columns = [
        {"label": "Item Name", "attr": "name", "clickable": True, "width": "25%"},
        {"label": "Description", "attr": "description", "clickable": False, "width": "35%"},
        {"label": "HSN Code", "attr": "hsn_code", "clickable": False, "width": "15%"},
        {"label": "Price", "attr": "price", "clickable": False, "width": "15%"},
        {"label": "Actions", "attr": "custom_actions", "clickable": False, "width": "10%"},
    ]

    context = {
        "object_list": items,
        "columns": columns,
        "add_url": reverse("item_create"),
        "list_title": "Item List",
        "object_name": "Item",
        "list_icon": "bi bi-box-seam",
    }

    return render(request, "masters/item/item_list.html", context)


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("item_list")
    else:
        form = ItemForm()
    # Pass an empty item context for template compatibility
    return render(request, "masters/item/item_form.html", {"form": form, "item": None})


@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("item_list")
    else:
        form = ItemForm(instance=item)

    context = {
        "form": form,
        "object": item,
        "title": "Edit Item",
        "form_title": "Edit Item",
        "list_url": reverse("item_list"),
        "add_url": reverse("item_create"),
    }

    return render(request, "masters/item/item_form.html", context)



@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    context = {
        "item": item,
        "object": item,
        "title": "Item Details",
        "object_name": "Item",
        "edit_url": reverse("item_edit", args=[item.id]),
        "delete_url": reverse("item_delete", args=[item.id]),
        "add_url": reverse("item_create"),
        "back_url": reverse("item_list"),
    }

    return render(request, "masters/item/item_detail.html", context)



@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect("item_list")
    return render(request, "masters/item/item_confirm_delete.html", {"item": item})


# ------------------ Customer Views ------------------ #
@login_required
def customer_list(request):
    customers = Customer.objects.all()

    for c in customers:
        c.address_display = f"{c.address.line1}, {c.address.city}" if c.address else ""
        c.contact_display = f"{c.contact.email} / {c.contact.phone}" if c.contact else ""
        c.get_edit_url = reverse("customer_edit", args=[c.id])
        c.get_delete_url = reverse("customer_delete", args=[c.id])

    columns = [
        {"label": "Name", "attr": "name", "clickable": True, "width": "22%"},
        {"label": "Address", "attr": "address_display", "clickable": False, "width": "25%"},
        {"label": "Contact", "attr": "contact_display", "clickable": False, "width": "25%"},
        {"label": "GSTIN", "attr": "gst_number", "clickable": False, "width": "18%"},
        {"label": "Actions", "attr": "custom_actions", "clickable": False, "width": "10%"},
    ]

    context = {
        "object_list": customers,
        "columns": columns,
        "add_url": reverse("customer_create"),
        "list_title": "Customer List",
        "object_name": "Customer",
        "list_icon": "bi bi-people",
    }

    return render(request, "masters/customer/customer_list.html", context)


@login_required
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm()
    return render(request, "masters/customer/customer_form.html", {"form": form})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    context = {
        "customer": customer,
        "object": customer,
        "title": "Customer Details",
        "object_name": "Customer",
        "edit_url": reverse("customer_edit", args=[customer.id]),
        "delete_url": reverse("customer_delete", args=[customer.id]),
        "add_url": reverse("customer_create"),
        "back_url": reverse("customer_list"),
    }

    return render(request, "masters/customer/customer_detail.html", context)



@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("customer_list")
    return render(
        request, "masters/customer/customer_confirm_delete.html", {"customer": customer}
    )


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)

    context = {
        "form": form,
        "object": customer,
        "title": "Edit Customer",
        "form_title": "Edit Customer",
        "list_url": reverse("customer_list"),
        "add_url": reverse("customer_create"),
    }

    return render(request, "masters/customer/customer_form.html", context)
