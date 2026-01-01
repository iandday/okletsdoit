from datetime import date
from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import FilterSchema
from ninja import Query
from ninja import Router
from ninja import Schema
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate

from core.auth import multi_auth

from .models import Question
from .models import QuestionCategory
from .models import QuestionURL
from .models import RsvpQuestion
from .models import RsvpQuestionChoice
from .models import Tips
from .models import WeddingSettings

User = get_user_model()

router = Router(tags=["Core"], auth=multi_auth)


# Schemas
class WeddingSettingsSchema(Schema):
    default_data_loaded: bool
    allow_rsvp: bool
    allow_photos: bool
    show_faq: bool
    wedding_date: Optional[date] = None
    rsvp_start_date: Optional[date] = None
    rsvp_end_date: Optional[date] = None
    rsvp_accept_button: str
    rsvp_decline_button: str
    rsvp_attending_label: str
    rsvp_accommodation_label: Optional[str] = None
    rsvp_vip_label: Optional[str] = None
    rsvp_accept_intro: str
    rsvp_accept_success_message: str
    rsvp_decline_success_message: str
    rsvp_accommodation_intro: Optional[str] = None
    rsvp_vip_intro: str
    rsvp_show_accommodation_intro: bool
    rsvp_show_vip_intro: bool
    rsvp_enable_email_updates: bool
    rsvp_email_update_label: Optional[str] = None
    rsvp_success_headline: str
    standard_group_label: str
    vip_group_label: str
    accommodation_group_label: str


class WeddingSettingsUpdateSchema(Schema):
    default_data_loaded: Optional[bool] = None
    allow_rsvp: Optional[bool] = None
    allow_photos: Optional[bool] = None
    wedding_date: Optional[date] = None
    show_faq: Optional[bool] = None
    rsvp_start_date: Optional[date] = None
    rsvp_end_date: Optional[date] = None
    rsvp_accept_button: Optional[str] = None
    rsvp_decline_button: Optional[str] = None
    rsvp_attending_label: Optional[str] = None
    rsvp_accommodation_label: Optional[str] = None
    rsvp_vip_label: Optional[str] = None
    rsvp_accept_intro: Optional[str] = None
    rsvp_accept_success_message: Optional[str] = None
    rsvp_decline_success_message: Optional[str] = None
    rsvp_accommodation_intro: Optional[str] = None
    rsvp_vip_intro: Optional[str] = None
    rsvp_show_accommodation_intro: Optional[bool] = None
    rsvp_show_vip_intro: Optional[bool] = None
    rsvp_enable_email_updates: Optional[bool] = None
    rsvp_email_update_label: Optional[str] = None
    rsvp_success_headline: Optional[str] = None
    standard_group_label: Optional[str] = None
    vip_group_label: Optional[str] = None
    accommodation_group_label: Optional[str] = None


# Question Schemas
class QuestionURLSchema(Schema):
    id: UUID
    url: str
    text: Optional[str] = None


class QuestionSchema(Schema):
    id: UUID
    category: str
    question: str
    slug: Optional[str] = None
    answer: Optional[str] = None
    order: int
    icon: str
    urls: List[QuestionURLSchema]
    published: bool
    created_at: datetime
    updated_at: datetime


class QuestionFilterSchema(FilterSchema):
    category: Optional[str] = None
    published: Optional[bool] = None


class QuestionCreateSchema(Schema):
    category_id: Optional[UUID] = None
    question: str
    answer: Optional[str] = None
    order: Optional[int] = 0
    icon: Optional[str] = "question-circle"
    published: Optional[bool] = False


class QuestionUpdateSchema(Schema):
    category_id: Optional[UUID] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    order: Optional[int] = None
    icon: Optional[str] = None
    published: Optional[bool] = None


class QuestionURLCreateSchema(Schema):
    question_id: UUID
    url: str
    text: Optional[str] = None


class QuestionURLUpdateSchema(Schema):
    url: Optional[str] = None
    text: Optional[str] = None


# Tips Schemas
class TipsSchema(Schema):
    id: UUID
    category: str
    content: str
    order: int
    published: bool
    created_at: datetime
    updated_at: datetime


class TipsFilterSchema(FilterSchema):
    category: Optional[str] = None
    published: Optional[bool] = None


class TipsCreateSchema(Schema):
    category_id: UUID
    content: str
    order: Optional[int] = 0
    published: Optional[bool] = False


class TipsUpdateSchema(Schema):
    category_id: Optional[UUID] = None
    content: Optional[str] = None
    order: Optional[int] = None
    published: Optional[bool] = None


# Combined Category Content Schemas
class CategoryContentSchema(Schema):
    category_id: UUID
    category_name: str
    category_order: int
    questions: List[QuestionSchema]
    tips: List[TipsSchema]


# RsvpQuestion Schemas
class RsvpQuestionChoiceSchema(Schema):
    id: UUID
    choice_text: str
    order: int


class RsvpQuestionSchema(Schema):
    id: UUID
    text: str
    order: int
    published: bool
    question_type: str
    choices: List[RsvpQuestionChoiceSchema]
    created_at: datetime
    updated_at: datetime


class RsvpQuestionFilterSchema(FilterSchema):
    published: Optional[bool] = None
    question_type: Optional[str] = None


class RsvpQuestionCreateSchema(Schema):
    text: str
    order: Optional[int] = 0
    published: Optional[bool] = False
    question_type: str


class RsvpQuestionUpdateSchema(Schema):
    text: Optional[str] = None
    order: Optional[int] = None
    published: Optional[bool] = None
    question_type: Optional[str] = None


# RsvpQuestionChoice Schemas
class RsvpQuestionChoiceCreateSchema(Schema):
    question_id: UUID
    choice_text: str
    order: Optional[int] = 0


class RsvpQuestionChoiceUpdateSchema(Schema):
    choice_text: Optional[str] = None
    order: Optional[int] = None


# WeddingSettings Endpoints
@router.get("/wedding-settings", response=WeddingSettingsSchema)
def get_wedding_settings(request):
    """Get wedding settings (singleton)"""
    settings = WeddingSettings.load()
    return settings


@router.put("/wedding-settings", response=WeddingSettingsSchema)
def update_wedding_settings(request, payload: WeddingSettingsUpdateSchema):
    """Update wedding settings"""
    settings = WeddingSettings.load()

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(settings, attr, value)

    settings.save()
    return settings


# Question CRUD Endpoints
@router.get("/questions", response=List[QuestionSchema])
@paginate(PageNumberPagination, page_size=50)
def list_questions(request, filters: QuestionFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all questions (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    questions = Question.objects.filter(q).prefetch_related("urls").order_by("order", "-created_at")

    return [
        {
            "id": question.id,
            "category": question.category.name if question.category else "General",
            "question": question.question,
            "slug": question.slug,
            "answer": question.answer,
            "order": question.order,
            "icon": question.icon,
            "urls": [
                {"id": url.id, "url": url.url, "text": url.text} for url in question.urls.filter(is_deleted=False)
            ],
            "published": question.published,
            "created_at": question.created_at,
            "updated_at": question.updated_at,
        }
        for question in questions
    ]


@router.get("/questions/{question_id}", response=QuestionSchema)
def get_question(request, question_id: UUID):
    """Get a specific question by ID"""
    question = get_object_or_404(Question, id=question_id, is_deleted=False)
    urls = [{"id": url.id, "url": url.url, "text": url.text} for url in question.urls.filter(is_deleted=False)]
    return {
        "id": question.id,
        "category": question.category.name if question.category else "General",
        "question": question.question,
        "slug": question.slug,
        "answer": question.answer,
        "order": question.order,
        "icon": question.icon,
        "urls": urls,
        "published": question.published,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }


@router.post("/questions", response=QuestionSchema)
def create_question(request, payload: QuestionCreateSchema):
    """Create a new question"""
    data = payload.dict()
    category_id = data.pop("category_id", None)

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    if category_id:
        category = get_object_or_404(QuestionCategory, id=category_id, is_deleted=False)
        data["category"] = category

    question = Question.objects.create(**data)

    urls = [
        {"id": url.id, "url": url.url, "description": url.description} for url in question.urls.filter(is_deleted=False)
    ]

    return {
        "id": question.id,
        "category": question.category.name if question.category else "General",
        "question": question.question,
        "slug": question.slug,
        "answer": question.answer,
        "order": question.order,
        "icon": question.icon,
        "urls": urls,
        "published": question.published,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }


@router.put("/questions/{question_id}", response=QuestionSchema)
def update_question(request, question_id: UUID, payload: QuestionUpdateSchema):
    """Update a question"""
    question = get_object_or_404(Question, id=question_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)
    category_id = data.pop("category_id", None)

    for attr, value in data.items():
        setattr(question, attr, value)

    if category_id:
        category = get_object_or_404(QuestionCategory, id=category_id, is_deleted=False)
        question.category = category

    if request.user.is_authenticated:
        question.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            question.updated_by = admin_user
    question.save()

    urls = [{"id": url.id, "url": url.url, "text": url.text} for url in question.urls.filter(is_deleted=False)]

    return {
        "id": question.id,
        "category": question.category.name if question.category else "General",
        "question": question.question,
        "slug": question.slug,
        "answer": question.answer,
        "order": question.order,
        "icon": question.icon,
        "urls": urls,
        "published": question.published,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }


@router.delete("/questions/{question_id}")
def delete_question(request, question_id: UUID):
    """Soft delete a question"""
    question = get_object_or_404(Question, id=question_id, is_deleted=False)
    question.is_deleted = True
    if request.user.is_authenticated:
        question.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            question.updated_by = admin_user
    question.save()
    return {"success": True, "message": "Question deleted successfully"}


# QuestionURL CRUD Endpoints
@router.get("/question-urls", response=List[QuestionURLSchema])
def list_question_urls(request, question_id: Optional[UUID] = None):
    """List all question URLs (non-deleted), optionally filtered by question_id"""
    queryset = QuestionURL.objects.filter(is_deleted=False)
    if question_id:
        queryset = queryset.filter(question_id=question_id)

    return [
        {
            "id": url.id,
            "url": url.url,
            "text": url.text,
        }
        for url in queryset
    ]


@router.get("/question-urls/{url_id}", response=QuestionURLSchema)
def get_question_url(request, url_id: UUID):
    """Get a specific question URL by ID"""
    url = get_object_or_404(QuestionURL, id=url_id, is_deleted=False)

    return {
        "id": url.id,
        "url": url.url,
        "text": url.text,
    }


@router.post("/question-urls", response=QuestionURLSchema)
def create_question_url(request, payload: QuestionURLCreateSchema):
    """Create a new question URL"""
    data = payload.dict()
    question_id = data.pop("question_id")

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    question = get_object_or_404(Question, id=question_id, is_deleted=False)
    data["question"] = question

    question_url = QuestionURL.objects.create(**data)

    # Add the URL to the question's urls many-to-many field
    question.urls.add(question_url)

    return {
        "id": question_url.id,
        "url": question_url.url,
        "text": question_url.text,
    }


@router.put("/question-urls/{url_id}", response=QuestionURLSchema)
def update_question_url(request, url_id: UUID, payload: QuestionURLUpdateSchema):
    """Update a question URL"""
    question_url = get_object_or_404(QuestionURL, id=url_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)

    for attr, value in data.items():
        setattr(question_url, attr, value)

    if request.user.is_authenticated:
        question_url.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            question_url.updated_by = admin_user

    question_url.save()

    return {
        "id": question_url.id,
        "url": question_url.url,
        "text": question_url.text,
    }


@router.delete("/question-urls/{url_id}")
def delete_question_url(request, url_id: UUID):
    """Soft delete a question URL"""
    question_url = get_object_or_404(QuestionURL, id=url_id, is_deleted=False)
    question_url.is_deleted = True
    if request.user.is_authenticated:
        question_url.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            question_url.updated_by = admin_user
    question_url.save()
    return {"success": True, "message": "Question URL deleted successfully"}


# Tips CRUD Endpoints
@router.get("/tips", response=List[TipsSchema])
@paginate(PageNumberPagination, page_size=50)
def list_tips(request, filters: TipsFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all tips (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    tips = Tips.objects.filter(q).select_related("category").order_by("order", "-created_at")

    return [
        {
            "id": tip.id,
            "category": tip.category.name if tip.category else "General",
            "content": tip.content,
            "order": tip.order,
            "published": tip.published,
            "created_at": tip.created_at,
            "updated_at": tip.updated_at,
        }
        for tip in tips
    ]


@router.get("/tips/{tip_id}", response=TipsSchema)
def get_tip(request, tip_id: UUID):
    """Get a specific tip by ID"""
    tip = get_object_or_404(Tips, id=tip_id, is_deleted=False)
    return {
        "id": tip.id,
        "category": tip.category.name if tip.category else "General",
        "content": tip.content,
        "order": tip.order,
        "published": tip.published,
        "created_at": tip.created_at,
        "updated_at": tip.updated_at,
    }


@router.post("/tips", response=TipsSchema)
def create_tip(request, payload: TipsCreateSchema):
    """Create a new tip"""
    data = payload.dict()
    category_id = data.pop("category_id")

    category = get_object_or_404(QuestionCategory, id=category_id, is_deleted=False)
    data["category"] = category

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user
    tip = Tips.objects.create(**data)
    return tip


@router.put("/tips/{tip_id}", response=TipsSchema)
def update_tip(request, tip_id: UUID, payload: TipsUpdateSchema):
    """Update a tip"""
    tip = get_object_or_404(Tips, id=tip_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)
    category_id = data.pop("category_id", None)

    for attr, value in data.items():
        setattr(tip, attr, value)

    if category_id:
        category = get_object_or_404(QuestionCategory, id=category_id, is_deleted=False)
        tip.category = category

    if request.user.is_authenticated:
        tip.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            tip.updated_by = admin_user
    tip.save()
    return tip


@router.delete("/tips/{tip_id}")
def delete_tip(request, tip_id: UUID):
    """Soft delete a tip"""
    tip = get_object_or_404(Tips, id=tip_id, is_deleted=False)
    tip.is_deleted = True
    if request.user.is_authenticated:
        tip.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            tip.updated_by = admin_user
    tip.save()
    return {"success": True, "message": "Tip deleted successfully"}


# Combined Category Content Endpoint
@router.get("/rsvp-categories-content", response=List[CategoryContentSchema])
def get_categories_content(request, published_only: bool = True):
    """Get all categories with their associated questions and tips"""
    q = Q(is_deleted=False)
    if published_only:
        q &= Q(published=True)

    categories = QuestionCategory.objects.filter(q).order_by("order", "name")

    result = []
    for category in categories:
        # Get questions for this category
        questions_q = Q(is_deleted=False, category=category)
        if published_only:
            questions_q &= Q(published=True)

        questions = Question.objects.filter(questions_q).prefetch_related("urls").order_by("order", "-created_at")
        questions_data = [
            {
                "id": question.id,
                "category": category.name,
                "question": question.question,
                "slug": question.slug,
                "answer": question.answer,
                "order": question.order,
                "icon": question.icon,
                "urls": [
                    {"id": url.id, "url": url.url, "text": url.text} for url in question.urls.filter(is_deleted=False)
                ],
                "published": question.published,
                "created_at": question.created_at,
                "updated_at": question.updated_at,
            }
            for question in questions
        ]

        # Get tips for this category
        tips_q = Q(is_deleted=False, category=category)
        if published_only:
            tips_q &= Q(published=True)

        tips = Tips.objects.filter(tips_q).order_by("order", "-created_at")
        tips_data = [
            {
                "id": tip.id,
                "category": category.name,
                "content": tip.content,
                "order": tip.order,
                "published": tip.published,
                "created_at": tip.created_at,
                "updated_at": tip.updated_at,
            }
            for tip in tips
        ]

        # Only include category if it has questions or tips
        if questions_data or tips_data:
            result.append(
                {
                    "category_id": category.id,
                    "category_name": category.name,
                    "category_order": category.order,
                    "questions": questions_data,
                    "tips": tips_data,
                }
            )

    return result


# RsvpQuestion CRUD Endpoints
@router.get("/rsvp-questions", response=List[RsvpQuestionSchema])
@paginate(PageNumberPagination, page_size=50)
def list_rsvp_questions(request, filters: RsvpQuestionFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all RSVP questions (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    questions = RsvpQuestion.objects.filter(q).prefetch_related("choices").order_by("order", "-created_at")

    result = []
    for question in questions:
        choices = [
            {"id": choice.id, "choice_text": choice.choice_text, "order": choice.order}
            for choice in question.choices.filter(is_deleted=False).order_by("order")
        ]
        result.append(
            {
                "id": question.id,
                "text": question.text,
                "order": question.order,
                "published": question.published,
                "question_type": question.question_type,
                "choices": choices,
                "created_at": question.created_at,
                "updated_at": question.updated_at,
            }
        )
    return result


@router.get("/rsvp-questions/{question_id}", response=RsvpQuestionSchema)
def get_rsvp_question(request, question_id: UUID):
    """Get a specific RSVP question by ID"""
    question = get_object_or_404(RsvpQuestion, id=question_id, is_deleted=False)
    choices = [
        {"id": choice.id, "choice_text": choice.choice_text, "order": choice.order}
        for choice in question.choices.filter(is_deleted=False).order_by("order")
    ]
    return {
        "id": question.id,
        "text": question.text,
        "order": question.order,
        "published": question.published,
        "question_type": question.question_type,
        "choices": choices,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }


@router.post("/rsvp-questions", response=RsvpQuestionSchema)
def create_rsvp_question(request, payload: RsvpQuestionCreateSchema):
    """Create a new RSVP question"""
    data = payload.dict()
    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user
    question = RsvpQuestion.objects.create(**data)
    return {
        "id": question.id,
        "text": question.text,
        "order": question.order,
        "published": question.published,
        "question_type": question.question_type,
        "choices": [],
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }


@router.put("/rsvp-questions/{question_id}", response=RsvpQuestionSchema)
def update_rsvp_question(request, question_id: UUID, payload: RsvpQuestionUpdateSchema):
    """Update an RSVP question"""
    question = get_object_or_404(RsvpQuestion, id=question_id, is_deleted=False)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(question, attr, value)

    if request.user.is_authenticated:
        question.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            question.updated_by = admin_user
    question.save()

    choices = [
        {"id": choice.id, "choice_text": choice.choice_text, "order": choice.order}
        for choice in question.choices.filter(is_deleted=False).order_by("order")
    ]
    return {
        "id": question.id,
        "text": question.text,
        "order": question.order,
        "published": question.published,
        "question_type": question.question_type,
        "choices": choices,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }


@router.delete("/rsvp-questions/{question_id}")
def delete_rsvp_question(request, question_id: UUID):
    """Soft delete an RSVP question"""
    question = get_object_or_404(RsvpQuestion, id=question_id, is_deleted=False)
    question.is_deleted = True
    if request.user.is_authenticated:
        question.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            question.updated_by = admin_user
    question.save()
    return {"success": True, "message": "RSVP question deleted successfully"}


# RsvpQuestionChoice CRUD Endpoints
@router.get("/rsvp-question-choices/{choice_id}", response=RsvpQuestionChoiceSchema)
def get_rsvp_question_choice(request, choice_id: UUID):
    """Get a specific RSVP question choice by ID"""
    choice = get_object_or_404(RsvpQuestionChoice, id=choice_id, is_deleted=False)
    return {
        "id": choice.id,
        "choice_text": choice.choice_text,
        "order": choice.order,
    }


@router.post("/rsvp-question-choices", response=RsvpQuestionChoiceSchema)
def create_rsvp_question_choice(request, payload: RsvpQuestionChoiceCreateSchema):
    """Create a new RSVP question choice"""
    data = payload.dict()
    question_id = data.pop("question_id")

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    choice = RsvpQuestionChoice.objects.create(question_id=question_id, **data)
    return {
        "id": choice.id,
        "choice_text": choice.choice_text,
        "order": choice.order,
    }


@router.put("/rsvp-question-choices/{choice_id}", response=RsvpQuestionChoiceSchema)
def update_rsvp_question_choice(request, choice_id: UUID, payload: RsvpQuestionChoiceUpdateSchema):
    """Update an RSVP question choice"""
    choice = get_object_or_404(RsvpQuestionChoice, id=choice_id, is_deleted=False)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(choice, attr, value)

    if request.user.is_authenticated:
        choice.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            choice.updated_by = admin_user
    choice.save()
    return {
        "id": choice.id,
        "choice_text": choice.choice_text,
        "order": choice.order,
    }


@router.delete("/rsvp-question-choices/{choice_id}")
def delete_rsvp_question_choice(request, choice_id: UUID):
    """Soft delete an RSVP question choice"""
    choice = get_object_or_404(RsvpQuestionChoice, id=choice_id, is_deleted=False)
    choice.is_deleted = True
    if request.user.is_authenticated:
        choice.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            choice.updated_by = admin_user
    choice.save()
    return {"success": True, "message": "RSVP question choice deleted successfully"}
