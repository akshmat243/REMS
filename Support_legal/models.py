from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from property.models import Property
from ai_utils import ask_openai
import uuid

User = get_user_model()

class RequestInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"requestinfo-{uuid.uuid4()}")
        super().save(*args, **kwargs)

class Feedback(models.Model):
    SENTIMENT_CHOICES = [('Positive', 'Positive'), ('Neutral', 'Neutral'), ('Negative', 'Negative')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    ai_sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"feedback-{uuid.uuid4()}")
        super().save(*args, **kwargs)

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
    PRIORITY_CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=50)
    ai_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"grievance-{uuid.uuid4()}")
        super().save(*args, **kwargs)

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

class SummonsNotice(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Resolved', 'Resolved'), ('Dismissed', 'Dismissed')]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    issued_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"summon-{uuid.uuid4()}")
        super().save(*args, **kwargs)

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

