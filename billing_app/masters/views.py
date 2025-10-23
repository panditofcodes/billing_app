from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Company, Item, Customer
from .forms import CompanyForm, ItemForm, CustomerForm


# ------------------ Company Views ------------------ #
@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(
        request, "masters/company/company_list.html", {"companies": companies}
    )


@login_required
def company_detail(request, pk):
    company = Company.objects.get(id=pk)
    return render(request, "masters/company/company_detail.html", {"company": company})


@login_required
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("company_list")
    else:
        form = CompanyForm()
    return render(request, "masters/company/company_form.html", {"form": form})


@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        company.delete()
        return redirect("company_list")
    return render(
        request, "masters/company/company_confirm_delete.html", {"company": company}
    )


# ------------------ Item Views ------------------ #
@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, "masters/item/item_list.html", {"items": items})


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("item_list")
    else:
        form = ItemForm()
    return render(request, "masters/item/item_form.html", {"form": form})


@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, id=pk)
    return render(request, "masters/item/item_detail.html", {"item": item})


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
    return render(
        request, "masters/customer/customer_list.html", {"customers": customers}
    )


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
    customer = get_object_or_404(Customer, id=pk)
    return render(
        request, "masters/customer/customer_detail.html", {"customer": customer}
    )


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("customer_list")
    return render(
        request, "masters/customer/customer_confirm_delete.html", {"customer": customer}
    )
