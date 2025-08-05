from django.contrib import admin
from .models import (
    RequestInfo, Feedback, ReportProblem, Testimonial, Grievance,
    CustomerServiceLog, SummonsNotice, ChatInteractionLog
)

@admin.register(RequestInfo)
class RequestInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'created_at']
    search_fields = ['user__full_name', 'property__title']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'submitted_at', 'ai_sentiment']
    list_filter = ['ai_sentiment', 'rating']

@admin.register(ReportProblem)
class ReportProblemAdmin(admin.ModelAdmin):
    list_display = ['user', 'related_property', 'created_at']
    search_fields = ['user__full_name', 'issue']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['user', 'approved', 'submitted_at', 'ai_sentiment']
    list_filter = ['approved', 'ai_sentiment']

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'ai_priority', 'created_at']
    list_filter = ['status', 'ai_priority']

@admin.register(CustomerServiceLog)
class CustomerServiceLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'handled_by', 'timestamp']
    search_fields = ['user__full_name', 'handled_by__full_name']

@admin.register(SummonsNotice)
class SummonsNoticeAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'issued_date', 'status']
    list_filter = ['status']

@admin.register(ChatInteractionLog)
class ChatInteractionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp']
    search_fields = ['user__full_name', 'query']
