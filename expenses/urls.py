from django.urls import path

from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.summary, name="summary"),
    path("create", views.create, name="create"),
    path("list", views.list, name="list"),
    path("expense_data", views.expense_data, name="expense_data"),
    path("import", views.expense_import, name="import"),
    path("template_download", views.template_download, name="template_download"),
    path("category/list", views.category_list, name="category_list"),
    path("category/create", views.category_create, name="category_create"),
    path("category/<slug:slug>/edit", views.category_edit, name="category_edit"),
    path("category/<slug:slug>/delete", views.category_delete, name="category_delete"),
]
