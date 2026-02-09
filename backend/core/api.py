from datetime import date
from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import FilterSchema, Query, Router, Schema
from ninja.files import UploadedFile
from ninja.pagination import PageNumberPagination, paginate

from core.auth import multi_auth

from .models import Idea
from .models import Inspiration
from .models import Question
from .models import QuestionCategory
from .models import QuestionURL
from .models import RsvpQuestion
from .models import RsvpQuestionChoice
from .models import Timeline
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
    show_venue: bool
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
    venue_page_title: str
    venue_page_description: str
    venue_name: str
    venue_address_line_one: str
    venue_address_line_two: Optional[str] = None
    venue_city: str
    venue_state: str
    venue_zipcode: str
    venue_country: str
    venue_parking: Optional[str] = None
    venue_gallery_title: str
    venue_gallery_description: str


class WeddingSettingsUpdateSchema(Schema):
    default_data_loaded: Optional[bool] = None
    allow_rsvp: Optional[bool] = None
    allow_photos: Optional[bool] = None
    wedding_date: Optional[date] = None
    show_faq: Optional[bool] = None
    show_venue: Optional[bool] = None
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
    venue_page_title: Optional[str] = None
    venue_page_description: Optional[str] = None
    venue_name: Optional[str] = None
    venue_address_line_one: Optional[str] = None
    venue_address_line_two: Optional[str] = None
    venue_city: Optional[str] = None
    venue_state: Optional[str] = None
    venue_zipcode: Optional[str] = None
    venue_country: Optional[str] = None
    venue_parking: Optional[str] = None
    venue_gallery_title: Optional[str] = None
    venue_gallery_description: Optional[str] = None


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


# Inspiration Schemas
class InspirationSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class InspirationFilterSchema(FilterSchema):
    name: Optional[str] = None


class InspirationCreateSchema(Schema):
    name: str
    description: Optional[str] = None


class InspirationUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None


class IdeaSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    created_by_id: Optional[UUID] = None
    created_by_name: Optional[str] = None
    updated_by_id: Optional[UUID] = None
    updated_by_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class IdeaFilterSchema(FilterSchema):
    name: Optional[str] = None


class IdeaCreateSchema(Schema):
    name: str
    description: Optional[str] = None


class IdeaUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None


# Timeline Schemas
class TimelineSchema(Schema):
    id: UUID
    name: str
    slug: str
    start: datetime
    end: Optional[datetime] = None
    order: int
    published: bool
    confirmed: bool
    description: Optional[str] = None
    created_by_id: Optional[UUID] = None
    created_by_name: Optional[str] = None
    updated_by_id: Optional[UUID] = None
    updated_by_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TimelineFilterSchema(FilterSchema):
    name: Optional[str] = None
    published: Optional[bool] = None
    confirmed: Optional[bool] = None


class TimelineCreateSchema(Schema):
    name: str
    start: datetime
    end: Optional[datetime] = None
    order: Optional[int] = 0
    published: Optional[bool] = False
    confirmed: Optional[bool] = False
    description: Optional[str] = None


class TimelineUpdateSchema(Schema):
    name: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    order: Optional[int] = None
    published: Optional[bool] = None
    confirmed: Optional[bool] = None
    description: Optional[str] = None


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


# Inspiration CRUD Endpoints
@router.get("/inspirations", response=List[InspirationSchema])
@paginate(PageNumberPagination, page_size=50)
def list_inspirations(request, filters: InspirationFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all inspirations (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    inspirations = Inspiration.objects.filter(q).order_by("name")

    return [
        {
            "id": inspiration.id,
            "name": inspiration.name,
            "slug": inspiration.slug,
            "description": inspiration.description,
            "image": inspiration.image.url if inspiration.image else None,
            "created_at": inspiration.created_at,
            "updated_at": inspiration.updated_at,
        }
        for inspiration in inspirations
    ]


@router.get("/inspirations/{inspiration_id}", response=InspirationSchema)
def get_inspiration(request, inspiration_id: UUID):
    """Get a specific inspiration by ID"""
    inspiration = get_object_or_404(Inspiration, id=inspiration_id, is_deleted=False)
    return {
        "id": inspiration.id,
        "name": inspiration.name,
        "slug": inspiration.slug,
        "description": inspiration.description,
        "image": inspiration.image.url if inspiration.image else None,
        "created_at": inspiration.created_at,
        "updated_at": inspiration.updated_at,
    }


@router.post("/inspirations", response=InspirationSchema)
def create_inspiration(request, payload: InspirationCreateSchema):
    """Create a new inspiration"""
    data = payload.dict()

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    inspiration = Inspiration.objects.create(**data)

    return {
        "id": inspiration.id,
        "name": inspiration.name,
        "slug": inspiration.slug,
        "description": inspiration.description,
        "image": inspiration.image.url if inspiration.image else None,
        "created_at": inspiration.created_at,
        "updated_at": inspiration.updated_at,
    }


@router.put("/inspirations/{inspiration_id}", response=InspirationSchema)
def update_inspiration(request, inspiration_id: UUID, payload: InspirationUpdateSchema):
    """Update an inspiration"""
    inspiration = get_object_or_404(Inspiration, id=inspiration_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)

    for attr, value in data.items():
        setattr(inspiration, attr, value)

    if request.user.is_authenticated:
        inspiration.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            inspiration.updated_by = admin_user

    inspiration.save()

    return {
        "id": inspiration.id,
        "name": inspiration.name,
        "slug": inspiration.slug,
        "description": inspiration.description,
        "image": inspiration.image.url if inspiration.image else None,
        "created_at": inspiration.created_at,
        "updated_at": inspiration.updated_at,
    }


@router.delete("/inspirations/{inspiration_id}")
def delete_inspiration(request, inspiration_id: UUID):
    """Soft delete an inspiration"""
    inspiration = get_object_or_404(Inspiration, id=inspiration_id, is_deleted=False)
    inspiration.is_deleted = True
    if request.user.is_authenticated:
        inspiration.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            inspiration.updated_by = admin_user
    inspiration.save()
    return {"success": True, "message": "Inspiration deleted successfully"}


@router.post("/inspirations/{inspiration_id}/upload-image", response=InspirationSchema)
def upload_inspiration_image(request, inspiration_id: UUID, image: UploadedFile):
    """Upload or update image for an inspiration"""
    inspiration = get_object_or_404(Inspiration, id=inspiration_id, is_deleted=False)

    # Delete old image if exists
    if inspiration.image:
        inspiration.image.delete(save=False)

    # Save new image
    inspiration.image = image

    if request.user.is_authenticated:
        inspiration.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            inspiration.updated_by = admin_user

    inspiration.save()

    return {
        "id": inspiration.id,
        "name": inspiration.name,
        "slug": inspiration.slug,
        "description": inspiration.description,
        "image": inspiration.image.url if inspiration.image else None,
        "created_at": inspiration.created_at,
        "updated_at": inspiration.updated_at,
    }


@router.delete("/inspirations/{inspiration_id}/image")
def delete_inspiration_image(request, inspiration_id: UUID):
    """Delete image from an inspiration"""
    inspiration = get_object_or_404(Inspiration, id=inspiration_id, is_deleted=False)

    if inspiration.image:
        inspiration.image.delete(save=False)
        inspiration.image = None

        if request.user.is_authenticated:
            inspiration.updated_by = request.user
        else:
            admin_user = User.objects.filter(is_staff=True, is_active=True).first()
            if admin_user:
                inspiration.updated_by = admin_user

        inspiration.save()
        return {"success": True, "message": "Image deleted successfully"}

    return {"success": False, "message": "No image to delete"}


# Idea CRUD Endpoints
@router.get("/ideas", response=List[IdeaSchema])
@paginate(PageNumberPagination, page_size=50)
def list_ideas(request, filters: IdeaFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all ideas (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    ideas = Idea.objects.filter(q).order_by("name")

    return [
        {
            "id": idea.id,
            "name": idea.name,
            "slug": idea.slug,
            "description": idea.description,
            "created_by_id": idea.created_by.id if idea.created_by else None,
            "created_by_name": idea.created_by.get_full_name() if idea.created_by else None,
            "updated_by_id": idea.updated_by.id if idea.updated_by else None,
            "updated_by_name": idea.updated_by.get_full_name() if idea.updated_by else None,
            "created_at": idea.created_at,
            "updated_at": idea.updated_at,
        }
        for idea in ideas
    ]


@router.get("/ideas/{idea_id}", response=IdeaSchema)
def get_idea(request, idea_id: UUID):
    """Get a specific idea by ID"""
    idea = get_object_or_404(Idea, id=idea_id, is_deleted=False)
    return {
        "id": idea.id,
        "name": idea.name,
        "slug": idea.slug,
        "description": idea.description,
        "created_by_id": idea.created_by.id if idea.created_by else None,
        "created_by_name": idea.created_by.get_full_name() if idea.created_by else None,
        "updated_by_id": idea.updated_by.id if idea.updated_by else None,
        "updated_by_name": idea.updated_by.get_full_name() if idea.updated_by else None,
        "created_at": idea.created_at,
        "updated_at": idea.updated_at,
    }


@router.post("/ideas", response=IdeaSchema)
def create_idea(request, payload: IdeaCreateSchema):
    """Create a new idea"""
    data = payload.dict()

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    idea = Idea.objects.create(**data)

    return {
        "id": idea.id,
        "name": idea.name,
        "slug": idea.slug,
        "description": idea.description,
        "created_by_id": idea.created_by.id if idea.created_by else None,
        "created_by_name": idea.created_by.get_full_name() if idea.created_by else None,
        "updated_by_id": idea.updated_by.id if idea.updated_by else None,
        "updated_by_name": idea.updated_by.get_full_name() if idea.updated_by else None,
        "created_at": idea.created_at,
        "updated_at": idea.updated_at,
    }


@router.put("/ideas/{idea_id}", response=IdeaSchema)
def update_idea(request, idea_id: UUID, payload: IdeaUpdateSchema):
    """Update an idea"""
    idea = get_object_or_404(Idea, id=idea_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)

    for attr, value in data.items():
        setattr(idea, attr, value)

    if request.user.is_authenticated:
        idea.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            idea.updated_by = admin_user

    idea.save()

    return {
        "id": idea.id,
        "name": idea.name,
        "slug": idea.slug,
        "description": idea.description,
        "created_by_id": idea.created_by.id if idea.created_by else None,
        "created_by_name": idea.created_by.get_full_name() if idea.created_by else None,
        "updated_by_id": idea.updated_by.id if idea.updated_by else None,
        "updated_by_name": idea.updated_by.get_full_name() if idea.updated_by else None,
        "created_at": idea.created_at,
        "updated_at": idea.updated_at,
    }


@router.delete("/ideas/{idea_id}")
def delete_idea(request, idea_id: UUID):
    """Soft delete an idea"""
    idea = get_object_or_404(Idea, id=idea_id, is_deleted=False)
    idea.is_deleted = True
    if request.user.is_authenticated:
        idea.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            idea.updated_by = admin_user
    idea.save()
    return {"success": True, "message": "Idea deleted successfully"}


# Timeline CRUD Endpoints
@router.get("/timelines", response=List[TimelineSchema])
@paginate(PageNumberPagination, page_size=50)
def list_timelines(request, filters: TimelineFilterSchema = Query(...)):  # pyright: ignore[reportCallIssue]
    """List all timeline events (non-deleted)"""
    q = Q(is_deleted=False)
    q &= filters.get_filter_expression()
    timelines = Timeline.objects.filter(q).order_by("order", "start")

    return [
        {
            "id": timeline.id,
            "name": timeline.name,
            "slug": timeline.slug,
            "start": timeline.start,
            "end": timeline.end,
            "order": timeline.order,
            "published": timeline.published,
            "confirmed": timeline.confirmed,
            "description": timeline.description,
            "created_by_id": timeline.created_by.id if timeline.created_by else None,
            "created_by_name": timeline.created_by.get_full_name() if timeline.created_by else None,
            "updated_by_id": timeline.updated_by.id if timeline.updated_by else None,
            "updated_by_name": timeline.updated_by.get_full_name() if timeline.updated_by else None,
            "created_at": timeline.created_at,
            "updated_at": timeline.updated_at,
        }
        for timeline in timelines
    ]


@router.get("/timelines/{timeline_id}", response=TimelineSchema)
def get_timeline(request, timeline_id: UUID):
    """Get a specific timeline event by ID"""
    timeline = get_object_or_404(Timeline, id=timeline_id, is_deleted=False)
    return {
        "id": timeline.id,
        "name": timeline.name,
        "slug": timeline.slug,
        "start": timeline.start,
        "end": timeline.end,
        "order": timeline.order,
        "published": timeline.published,
        "confirmed": timeline.confirmed,
        "description": timeline.description,
        "created_by_id": timeline.created_by.id if timeline.created_by else None,
        "created_by_name": timeline.created_by.get_full_name() if timeline.created_by else None,
        "updated_by_id": timeline.updated_by.id if timeline.updated_by else None,
        "updated_by_name": timeline.updated_by.get_full_name() if timeline.updated_by else None,
        "created_at": timeline.created_at,
        "updated_at": timeline.updated_at,
    }


@router.post("/timelines", response=TimelineSchema)
def create_timeline(request, payload: TimelineCreateSchema):
    """Create a new timeline event"""
    data = payload.dict()

    if request.user.is_authenticated:
        data["created_by"] = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            data["created_by"] = admin_user

    timeline = Timeline.objects.create(**data)

    return {
        "id": timeline.id,
        "name": timeline.name,
        "slug": timeline.slug,
        "start": timeline.start,
        "end": timeline.end,
        "order": timeline.order,
        "published": timeline.published,
        "confirmed": timeline.confirmed,
        "description": timeline.description,
        "created_by_id": timeline.created_by.id if timeline.created_by else None,
        "created_by_name": timeline.created_by.get_full_name() if timeline.created_by else None,
        "updated_by_id": timeline.updated_by.id if timeline.updated_by else None,
        "updated_by_name": timeline.updated_by.get_full_name() if timeline.updated_by else None,
        "created_at": timeline.created_at,
        "updated_at": timeline.updated_at,
    }


@router.put("/timelines/{timeline_id}", response=TimelineSchema)
def update_timeline(request, timeline_id: UUID, payload: TimelineUpdateSchema):
    """Update a timeline event"""
    timeline = get_object_or_404(Timeline, id=timeline_id, is_deleted=False)
    data = payload.dict(exclude_unset=True)

    for attr, value in data.items():
        setattr(timeline, attr, value)

    if request.user.is_authenticated:
        timeline.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            timeline.updated_by = admin_user

    timeline.save()

    return {
        "id": timeline.id,
        "name": timeline.name,
        "slug": timeline.slug,
        "start": timeline.start,
        "end": timeline.end,
        "order": timeline.order,
        "published": timeline.published,
        "confirmed": timeline.confirmed,
        "description": timeline.description,
        "created_by_id": timeline.created_by.id if timeline.created_by else None,
        "created_by_name": timeline.created_by.get_full_name() if timeline.created_by else None,
        "updated_by_id": timeline.updated_by.id if timeline.updated_by else None,
        "updated_by_name": timeline.updated_by.get_full_name() if timeline.updated_by else None,
        "created_at": timeline.created_at,
        "updated_at": timeline.updated_at,
    }


@router.delete("/timelines/{timeline_id}")
def delete_timeline(request, timeline_id: UUID):
    """Soft delete a timeline event"""
    timeline = get_object_or_404(Timeline, id=timeline_id, is_deleted=False)
    timeline.is_deleted = True
    if request.user.is_authenticated:
        timeline.updated_by = request.user
    else:
        admin_user = User.objects.filter(is_staff=True, is_active=True).first()
        if admin_user:
            timeline.updated_by = admin_user
    timeline.save()
    return {"success": True, "message": "Timeline event deleted successfully"}
