from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from property.models import Property
import uuid
from django.conf import settings

User = get_user_model()

class AgentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="agent_profile")
    specialization = models.CharField(max_length=255, blank=True)   # main specialization
    specialties = models.JSONField(default=list, blank=True)         # multiple tags (Residential, Commercial, etc.)
    languages = models.JSONField(default=list, blank=True)           # multiple tags (English, Hindi, etc.)

    experience_years = models.PositiveIntegerField(default=0)
    deals_closed = models.PositiveIntegerField(default=0)
    properties_handled = models.PositiveIntegerField(default=0)      # total properties posted/managed

    rating = models.FloatField(default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(default=False)
    response_time = models.CharField(max_length=50, default="Within 24 hours")  # like "Within 2 hours"

    profile_image = models.ImageField(upload_to="agent_profiles/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    about = models.TextField(blank=True, null=True)

    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f"Agent: {self.user.full_name}"


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.full_name}-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def update_rating_and_reviews(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = round(reviews.aggregate(models.Avg("rating"))["rating__avg"], 2)
            self.total_reviews = reviews.count()
        else:
            self.rating = 0.0
            self.total_reviews = 0
        self.save(update_fields=["rating", "total_reviews"])


class AgentReview(models.Model):
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1–5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.agent.update_rating_and_reviews()

    def __str__(self):
        return f"{self.user.full_name} → {self.agent.user.full_name} ({self.rating})"



class Lead(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Interested', 'Interested'),
        ('Not Interested', 'Not Interested'),
        ('Converted', 'Converted'),
        ('Closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    interested_in = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='New')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class InteractionLog(models.Model):
    INTERACTION_CHOICES = [
        ('Call', 'Call'),
        ('Email', 'Email'),
        ('Meeting', 'Meeting'),
        ('Site Visit', 'Site Visit'),
        ('WhatsApp', 'WhatsApp'),
        ('Other', 'Other'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_CHOICES)
    notes = models.TextField()
    date = models.DateTimeField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"interaction-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lead.name} - {self.interaction_type}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"notif-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"To {self.user.username}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ('user', 'property')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"wishlist-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.full_name} ♥ {self.property.title}"

class PropertyComparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property_1 = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='compared_as_first')
    property_2 = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='compared_as_second')
    compared_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ('user', 'property_1', 'property_2')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"compare-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}: {self.property_1.title} vs {self.property_2.title}"
