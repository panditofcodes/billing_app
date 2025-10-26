from django.urls import path
from . import views

urlpatterns = [
    # ------------------ Company URLs ------------------ #
    path("companies/", views.company_list, name="company_list"),
    path("companies/new/", views.company_create, name="company_create"),
    path("companies/<int:pk>/", views.company_detail, name="company_detail"),
    path("companies/<int:pk>/delete/", views.company_delete, name="company_delete"),
    path("companies/<int:pk>/edit/", views.company_edit, name="company_edit"),
    # ------------------ Address URLs ------------------ #
    path("addresses/new/", views.address_create, name="address_create"),
    path(
        "addresses/ajax/create/", views.address_create_ajax, name="address_create_ajax"
    ),
    # ------------------ Contact URLs ------------------ #
    path("contacts/new/", views.contact_create, name="contact_create"),
    path(
        "contacts/ajax/create/", views.contact_create_ajax, name="contact_create_ajax"
    ),
    # ------------------ Item URLs ------------------ #
    path("items/", views.item_list, name="item_list"),
    path("items/new/", views.item_create, name="item_create"),
    path("items/<int:pk>/", views.item_detail, name="item_detail"),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path("items/<int:pk>/delete/", views.item_delete, name="item_delete"),
    # ------------------ Customer URLs ------------------ #
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/new/", views.customer_create, name="customer_create"),
    path("customers/<int:pk>/", views.customer_detail, name="customer_detail"),
    path("customers/<int:pk>/delete/", views.customer_delete, name="customer_delete"),
    path("customers/<int:pk>/edit/", views.customer_edit, name="customer_edit"),
]
