from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from property.models import Property
from ai_utils import ask_openai
import uuid
from django.conf import settings
from django.utils import timezone

User = get_user_model()

class RequestInfo(models.Model):
    INFO_TYPES = [
        ("property_details", "Property Details & Pricing"),
        ("market_analysis", "Market Analysis Report"),
        ("investment_opportunities", "Investment Opportunities"),
        ("loan_finance", "Loan & Finance Assistance"),
        ("legal_help", "Legal Documentation Help"),
        ("site_visit", "Site Visit Arrangement"),
    ]

    PROPERTY_TYPES = [
        ("apartment", "Apartment"),
        ("villa", "Villa"),
        ("plot", "Plot"),
        ("commercial", "Commercial"),
        ("other", "Other"),
    ]

    BUDGET_RANGES = [
        ("0-20L", "0 - 20 Lakhs"),
        ("20L-50L", "20 Lakhs - 50 Lakhs"),
        ("50L-1Cr", "50 Lakhs - 1 Crore"),
        ("1Cr+", "Above 1 Crore"),
    ]

    COMMUNICATION_METHODS = [
        ("email", "Email"),
        ("phone", "Phone Call"),
        ("whatsapp", "WhatsApp"),
    ]

    TIMELINE_CHOICES = [
        ("immediate", "Immediate"),
        ("1-3m", "1 - 3 Months"),
        ("3-6m", "3 - 6 Months"),
        ("6m+", "6+ Months"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True, null=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, blank=True, null=True)
    budget_range = models.CharField(max_length=50, choices=BUDGET_RANGES, blank=True, null=True)
    preferred_location = models.CharField(max_length=200, blank=True, null=True)
    specific_requirements = models.TextField(blank=True, null=True)

    # multiple selections (M2M)
    info_types = models.JSONField(default=list, blank=True)  

    communication_method = models.CharField(max_length=20, choices=COMMUNICATION_METHODS, default="email")
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES, blank=True, null=True)

    consent = models.BooleanField(default=False)  # agree checkbox
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Inquiry from {self.full_name} - {self.email}"

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ("general", "General Feedback"),
        ("feature", "Feature Request"),
        ("bug", "Bug Report"),
        ("compliment", "Compliment"),
    ]

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, default="general")
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)

    # User Info
    name = models.CharField(max_length=150)
    email = models.EmailField()

    # Feedback Details
    subject = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    detailed_feedback = models.TextField(blank=True, null=True)

    # Additional Questions
    what_went_well = models.TextField(blank=True, null=True)
    how_to_improve = models.TextField(blank=True, null=True)
    recommend_us = models.CharField(max_length=50, blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feedback_type} - {self.subject} ({self.name})"

class ReportProblem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.TextField()
    related_property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"report-{uuid.uuid4()}")
        super().save(*args, **kwargs)

class Testimonial(models.Model):
    SENTIMENT_CHOICES = [('Positive', 'Positive'), ('Neutral', 'Neutral'), ('Negative', 'Negative')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    ai_sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"testimonial-{uuid.uuid4()}")
        super().save(*args, **kwargs)

class Grievance(models.Model):
    PRIORITY_LEVELS = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="grievances"
    )
    category = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default="low")
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Optional reference fields
    property_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    # File uploads (multiple evidence allowed)
    evidence = models.FileField(upload_to="grievance_evidence/", blank=True, null=True)

    # Tracking fields
    status = models.CharField(
        max_length=20,
        choices=[
            ("open", "Open"),
            ("in_progress", "In Progress"),
            ("resolved", "Resolved"),
            ("closed", "Closed"),
        ],
        default="open"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.priority})"

class CustomerServiceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_taken = models.TextField()
    handled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='handled_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"csl-{uuid.uuid4()}")
        super().save(*args, **kwargs)


class NoticeResponse(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Resolved', 'Resolved'), ('Dismissed', 'Dismissed')]
    RESPONSE_TYPES = [
        ("compliance", "Compliance Confirmation"),
        ("objection", "Objection"),
        ("clarification", "Request for Clarification"),
        ("document", "Document Submission"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="notice_responses"
    )
    notice_id = models.CharField(max_length=100)  
    response_type = models.CharField(max_length=30, choices=RESPONSE_TYPES)
    response_details = models.TextField()

    supporting_document = models.FileField(upload_to="notice_responses/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"summon-{uuid.uuid4()}")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Response to Notice {self.notice_id} - {self.response_type}"

class ChatInteractionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"chatlog-{uuid.uuid4()}")

        if not self.ai_response and self.query:
            try:
                self.ai_response = ask_openai(self.query)
            except Exception as e:
                self.ai_response = f"[AI Error: {str(e)}]"

        super().save(*args, **kwargs)

class SupportTicket(models.Model):
    CATEGORY_CHOICES = [
        ("property_search", "Property Search"),
        ("documentation", "Documentation"),
        ("technical_issues", "Technical Issues"),
        ("account_support", "Account Support"),
        ("other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    subject = models.CharField(max_length=255)
    message = models.TextField()

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: link to registered user (if logged in users can submit tickets)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="support_tickets")

    def __str__(self):
        return f"Ticket {self.subject} ({self.priority})"