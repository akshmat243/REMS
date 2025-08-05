from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from property.models import Property
import uuid

User = get_user_model()

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
        return f"{self.user.username} ♥ {self.property.title}"

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
