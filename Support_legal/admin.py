from django.contrib import admin
from .models import (
    RequestInfo, Feedback, ProblemReport, Testimonial, Grievance,
    CustomerServiceLog, NoticeResponse, ChatInteractionLog, SupportTicket
)

from django.contrib import admin
from .models import RequestInfo


@admin.register(RequestInfo)
class RequestInfoAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone_number",
        "property_type",
        "budget_range",
        "communication_method",
        "timeline",
        "consent",
        "created_at",
    )
    list_filter = (
        "property_type",
        "budget_range",
        "communication_method",
        "timeline",
        "consent",
        "created_at",
    )
    search_fields = ("full_name", "email", "phone_number", "city", "preferred_location")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Personal Info", {
            "fields": ("full_name", "email", "phone_number", "city"),
        }),
        ("Property Interest", {
            "fields": ("property_type", "budget_range", "preferred_location", "specific_requirements"),
        }),
        ("Request Details", {
            "fields": ("info_types", "communication_method", "timeline"),
        }),
        ("Consent & Meta", {
            "fields": ("consent", "created_at"),
        }),
    )

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone_number",
        "category",
        "priority",
        "subject",
        "created_at",
        "updated_at",
    )
    list_filter = ("category", "priority", "created_at")
    search_fields = ("full_name", "email", "phone_number", "subject", "message")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("User Info", {
            "fields": ("full_name", "email", "phone_number", "user")
        }),
        ("Ticket Details", {
            "fields": ("category", "priority", "subject", "message")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "feedback_type",
        "rating",
        "name",
        "email",
        "subject",
        "category",
        "created_at",
    )
    list_filter = ("feedback_type", "rating", "category", "created_at")
    search_fields = ("name", "email", "subject", "detailed_feedback")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("feedback_type", "rating", "name", "email", "subject", "category")
        }),
        ("Feedback Details", {
            "fields": ("detailed_feedback", "what_went_well", "how_to_improve", "recommend_us")
        }),
        ("Metadata", {
            "fields": ("created_at",)
        }),
    )

@admin.register(ProblemReport)
class ProblemReportAdmin(admin.ModelAdmin):
    list_display = (
        "id", "problem_type", "priority", "name", "email", "phone_number",
        "problem_summary", "created_at"
    )
    list_filter = ("problem_type", "priority", "created_at")
    search_fields = ("name", "email", "phone_number", "problem_summary")
    readonly_fields = ("created_at",)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['user', 'approved', 'submitted_at', 'ai_sentiment']
    list_filter = ['approved', 'ai_sentiment']

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "priority",
        "status",
        "user",
        "created_at",
        "updated_at",
    )
    list_filter = ("priority", "status", "category", "created_at")
    search_fields = ("title", "description", "property_id", "transaction_id", "user__email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "category", "priority", "description")
        }),
        ("References", {
            "fields": ("property_id", "transaction_id")
        }),
        ("Attachments", {
            "fields": ("evidence",)
        }),
        ("Tracking", {
            "fields": ("status", "user", "created_at", "updated_at")
        }),
    )

@admin.register(CustomerServiceLog)
class CustomerServiceLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'handled_by', 'timestamp']
    search_fields = ['user__full_name', 'handled_by__full_name']

@admin.register(NoticeResponse)
class NoticeResponseAdmin(admin.ModelAdmin):
    list_display = ("notice_id", "response_type", "user", "created_at", "updated_at")
    list_filter = ("response_type", "created_at")
    search_fields = ("notice_id", "response_details", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")

@admin.register(ChatInteractionLog)
class ChatInteractionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp']
    search_fields = ['user__full_name', 'query']
