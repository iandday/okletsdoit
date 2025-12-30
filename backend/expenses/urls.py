from django.urls import path

from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.summary, name="summary"),
    path("import", views.expense_import, name="import"),
    path("template_download", views.template_download, name="template_download"),
    path("create", views.create, name="create"),
    path("list", views.list, name="list"),
    path("expense_data", views.expense_data, name="expense_data"),
    path("expense_delete_modal/", views.expense_delete_modal, name="expense_delete_modal"),
    path("<slug:slug>", views.detail, name="detail"),
    path("<slug:slug>/edit", views.expense_edit, name="expense_edit"),
    path("<slug:slug>/delete", views.expense_delete, name="expense_delete"),
    path("category/create", views.category_create, name="category_create"),
    path("category_delete_modal/", views.category_delete_modal, name="category_delete_modal"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("category/<slug:slug>/edit", views.category_edit, name="category_edit"),
    path("category/<slug:slug>/delete", views.category_delete, name="category_delete"),
]
