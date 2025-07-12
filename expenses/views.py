from django.shortcuts import redirect, render
from django.db.models import Sum, Case, When, Value, DecimalField, F
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from expenses.forms import CategoryForm
from .models import Category, Expense


@login_required
def summary(request):
    # Get all categories with their expense totals and calculations
    categories = (
        Category.objects.filter(is_deleted=False)
        .annotate(total_estimated=Sum("expense__estimated_amount"), total_actual=Sum("expense__actual_amount"))
        .annotate(
            # Calculate variance
            variance=Case(
                When(
                    total_estimated__isnull=False,
                    total_actual__isnull=False,
                    then=F("total_actual") - F("total_estimated"),
                ),
                default=Value(None),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            # Calculate percentage
            percentage=Case(
                When(
                    total_estimated__gt=0,
                    total_actual__isnull=False,
                    then=(F("total_actual") / F("total_estimated")) * 100,
                ),
                default=Value(None),
                output_field=DecimalField(max_digits=5, decimal_places=1),
            ),
        )
        .order_by("name")
    )

    # Calculate overall totals
    overall_estimated = (
        Expense.objects.filter(is_deleted=False, estimated_amount__isnull=False).aggregate(
            total=Sum("estimated_amount")
        )["total"]
        or 0
    )

    overall_actual = (
        Expense.objects.filter(is_deleted=False, actual_amount__isnull=False).aggregate(total=Sum("actual_amount"))[
            "total"
        ]
        or 0
    )

    # Calculate variance and percentage
    variance = overall_actual - overall_estimated
    variance_percentage = (variance / overall_estimated * 100) if overall_estimated > 0 else 0

    # Add calculated fields to each category
    categories_with_calcs = []
    for category in categories:
        category_data = {
            "category": category,
            "total_estimated": category.total_estimated,
            "total_actual": category.total_actual,
            "variance": category.variance,
            "percentage": category.percentage,
            "progress_class": "progress-error"
            if category.percentage and category.percentage > 100
            else "progress-warning"
            if category.percentage and category.percentage > 80
            else "progress-success",
        }
        categories_with_calcs.append(category_data)

    context = {
        "categories": categories_with_calcs,
        "overall_estimated": overall_estimated,
        "overall_actual": overall_actual,
        "variance": variance,
        "variance_percentage": variance_percentage,
    }

    return render(request, "expenses/summary.html", context)


@login_required
def create(request):
    # Placeholder for create view logic
    return render(request, "expenses/create.html")


@login_required
def list(request):
    # check if category is in parameters
    category_slug = request.GET.get("category")
    if category_slug:
        category = Category.objects.filter(slug=category_slug, is_deleted=False)
        if not category:
            return redirect("expenses:category_list")
        expenses = Expense.objects.filter(category__slug=category_slug, is_deleted=False).order_by("-date")
        context = {"expenses": expenses, "category": category}
    else:
        expenses = Expense.objects.filter(is_deleted=False).order_by("-date")
        context = {"expenses": expenses}

    # Placeholder for list view logic
    return render(request, "expenses/list.html", context)


def category_list(request):
    categories = (
        Category.objects.filter(is_deleted=False)
        .prefetch_related("expense_set")
        .annotate(
            total_expenses=Count("expense", filter=Q(expense__is_deleted=False)),
            expenses_with_actual=Count(
                "expense", filter=Q(expense__actual_amount__isnull=False, expense__is_deleted=False)
            ),
            expenses_with_estimated=Count(
                "expense", filter=Q(expense__estimated_amount__isnull=False, expense__is_deleted=False)
            ),
        )
        .order_by("name")
    )

    form = CategoryForm()

    category_forms = {}
    for category in categories:
        category_forms[category.id] = CategoryForm(instance=category)

    return render(
        request,
        "expenses/category_list.html",
        {"categories": categories, "form": form, "category_forms": category_forms},
    )


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category: Category = form.save(commit=False)
            category.created_by = request.user
            category.save()
    return redirect("expenses:category_list")


def category_edit(request, slug: str):
    category = Category.objects.get(slug=slug, is_deleted=False)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.updated_by = request.user
            category.save()
    return redirect("expenses:category_list")


def category_delete(request, slug: str):
    category = Category.objects.get(slug=slug, is_deleted=False)
    if request.method == "POST":
        category.is_deleted = True
        category.save()
    return redirect("expenses:category_list")
