import logging
from datetime import date as Date
from datetime import datetime
from typing import List as TypeList
from typing import Optional
from uuid import UUID
from decimal import Decimal

from core.auth import multi_auth
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import FilterSchema
from ninja import Query
from ninja import Router
from ninja import Schema
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate

from .models import Category, Expense

router = Router(tags=["Expenses"], auth=multi_auth)

logger = logging.getLogger(__name__)

User = get_user_model()


# Category Schemas
class CategorySchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CategoryFilterSchema(FilterSchema):
    name: Optional[str] = None


class CategoryCreateSchema(Schema):
    name: str
    description: Optional[str] = ""


class CategoryUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None


# Expense Schemas
class ExpenseSchema(Schema):
    id: UUID
    item: str
    slug: str
    description: Optional[str] = None
    date: Optional[Date] = None
    category_id: Optional[UUID] = None
    vendor_id: Optional[UUID] = None
    quantity: int
    unit_price: Decimal
    additional_price: Decimal
    estimated_amount: Optional[Decimal] = None
    actual_amount: Optional[Decimal] = None
    url: Optional[str] = None
    purchased: bool
    variance: Optional[Decimal] = None
    calculated_price: Decimal
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def resolve_purchased(obj):
        return obj.purchased

    @staticmethod
    def resolve_variance(obj):
        return obj.variance

    @staticmethod
    def resolve_calculated_price(obj):
        return obj.calculated_price


class ExpenseFilterSchema(FilterSchema):
    item: Optional[str] = None
    category_id: Optional[UUID] = None
    vendor_id: Optional[UUID] = None


class ExpenseCreateSchema(Schema):
    item: str
    description: Optional[str] = ""
    date: Optional[Date] = None
    category_id: Optional[UUID] = None
    vendor_id: Optional[UUID] = None
    quantity: Optional[int] = 1
    unit_price: Optional[Decimal] = Decimal("0.00")
    additional_price: Optional[Decimal] = Decimal("0.00")
    estimated_amount: Optional[Decimal] = None
    actual_amount: Optional[Decimal] = None
    url: Optional[str] = None


class ExpenseUpdateSchema(Schema):
    item: Optional[str] = None
    description: Optional[str] = None
    date: Optional[Date] = None
    category_id: Optional[UUID] = None
    vendor_id: Optional[UUID] = None
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    additional_price: Optional[Decimal] = None
    estimated_amount: Optional[Decimal] = None
    actual_amount: Optional[Decimal] = None
    url: Optional[str] = None


# Category CRUD Endpoints
@router.get("/categories", response=TypeList[CategorySchema])
@paginate(PageNumberPagination, page_size=50)
def list_categories(request, filters: CategoryFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all categories (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    return Category.objects.filter(q).order_by("name")


@router.get("/categories/{category_id}", response=CategorySchema)
def get_category(request, category_id: UUID):
    """Get a specific category by ID"""
    return get_object_or_404(Category, id=category_id, is_deleted=False)


@router.post("/categories", response=CategorySchema)
def create_category(request, payload: CategoryCreateSchema):
    """Create a new category"""
    data = payload.dict()
    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user
    category = Category.objects.create(**data)
    return category


@router.put("/categories/{category_id}", response=CategorySchema)
def update_category(request, category_id: UUID, payload: CategoryUpdateSchema):
    """Update a category"""
    category = get_object_or_404(Category, id=category_id, is_deleted=False)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(category, attr, value)

    if request.user.is_authenticated:
        category.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            category.updated_by = admin_user
    category.save()
    return category


@router.delete("/categories/{category_id}")
def delete_category(request, category_id: UUID):
    """Soft delete a category"""
    category = get_object_or_404(Category, id=category_id, is_deleted=False)
    category.is_deleted = True
    if request.user.is_authenticated:
        category.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            category.updated_by = admin_user
    category.save()
    return {"success": True, "message": "Category deleted successfully"}


# Expense CRUD Endpoints
@router.get("/expenses", response=TypeList[ExpenseSchema])
@paginate(PageNumberPagination, page_size=50)
def list_expenses(request, filters: ExpenseFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all expenses (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    return Expense.objects.filter(q).order_by("-date", "item")


@router.get("/expenses/{expense_id}", response=ExpenseSchema)
def get_expense(request, expense_id: UUID):
    """Get a specific expense by ID"""
    return get_object_or_404(Expense, id=expense_id, is_deleted=False)


@router.post("/expenses", response=ExpenseSchema)
def create_expense(request, payload: ExpenseCreateSchema):
    """Create a new expense"""
    data = payload.dict()

    # Validate category_id if provided
    if data.get("category_id"):
        get_object_or_404(Category, id=data["category_id"], is_deleted=False)

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    expense = Expense.objects.create(**data)
    return expense


@router.put("/expenses/{expense_id}", response=ExpenseSchema)
def update_expense(request, expense_id: UUID, payload: ExpenseUpdateSchema):
    """Update an expense"""
    expense = get_object_or_404(Expense, id=expense_id, is_deleted=False)

    data = payload.dict(exclude_unset=True)

    # Validate category_id if it's being changed
    if "category_id" in data and data["category_id"]:
        get_object_or_404(Category, id=data["category_id"], is_deleted=False)

    for attr, value in data.items():
        setattr(expense, attr, value)

    if request.user.is_authenticated:
        expense.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            expense.updated_by = admin_user
    expense.save()
    return expense


@router.delete("/expenses/{expense_id}")
def delete_expense(request, expense_id: UUID):
    """Soft delete an expense"""
    expense = get_object_or_404(Expense, id=expense_id, is_deleted=False)
    expense.is_deleted = True
    if request.user.is_authenticated:
        expense.updated_by = request.user
    else:
        # Use first admin user for service token requests
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            expense.updated_by = admin_user
    expense.save()
    return {"success": True, "message": "Expense deleted successfully"}
