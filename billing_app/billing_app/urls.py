"""
URL configuration for billing_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# Dashboard view (requires login)
@login_required(login_url='login')
def dashboard(request):
    return render(request, "dashboard.html")  # Using your dashboard template

urlpatterns = [
    path("admin/", admin.site.urls),

    # Dashboard/Homepage (after login)
    path("", dashboard, name="dashboard"),

    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="login"),

    # App URLs
    path("masters/", include("masters.urls")),  # Companies, Items, Customers
    path("transactions/", include("transactions.urls")),  # Invoices
]
