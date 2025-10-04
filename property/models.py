from django.db import models
from django.utils.text import slugify
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model

# User = get_user_model()

class PropertyType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Address(models.Model):
    house_no = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.city}-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.house_no}, {self.area}, {self.city}"

class Property(models.Model):
    CATEGORY_CHOICES = [('Sale', 'Sale'), ('Rent', 'Rent'), ('Lease', 'Lease')]
    FURNISHING_CHOICES = [('Furnished', 'Furnished'), ('Semi-Furnished', 'Semi-Furnished'), ('Unfurnished', 'Unfurnished')]
    AVAILABILITY_STATUS = [('Ready to Move', 'Ready to Move'), ('Under Construction', 'Under Construction')]
    OWNERSHIP_TYPE = [('Freehold', 'Freehold'), ('Leasehold', 'Leasehold')]
    PROPERTY_STATUS = [('Pending', 'Pending for Approval'), ('Active', 'Active'), ('Sold', 'Sold'), ('Rented', 'Rented'), ('Inactive', 'Inactive')]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    area_sqft = models.FloatField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    balconies = models.IntegerField()
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES)
    floor_no = models.IntegerField()
    total_floors = models.IntegerField()
    availability_status = models.CharField(max_length=30, choices=AVAILABILITY_STATUS)
    possession_date = models.DateField()
    age_of_property = models.CharField(max_length=50)
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_TYPE)
    rera_approved = models.BooleanField(default=False)
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2)
    property_status = models.CharField(max_length=20, choices=PROPERTY_STATUS, blank=True, default='Pending')
    listed_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    price_negotiable = models.BooleanField(default=False)
    terms_and_conditions = models.BooleanField(default=False)

    # AI fields
    ai_price_estimate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ai_recommended_score = models.FloatField(null=True, blank=True)
    
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name="agent_properties"
    )

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ai_tag = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_title = getattr(self.property, "title", "property")
            self.slug = slugify(f"{base_title}-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{getattr(self.property, 'title', 'Property')} Image"

class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="property_videos/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"property-video-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Video for {self.property.title} ({self.caption})"

class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='amenities')
    amenity = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.amenity}-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.amenity

class PropertyDocument(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='property_documents/')
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    ai_extracted_text = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"doc-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.document_type} - {self.property.title}"

class PostedProperty(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    posted_date = models.DateTimeField(auto_now_add=True)
    review_comments = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"post-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.property.title}"

class PropertyContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="contacts")
    owner_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner_name} - {self.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.owner_name)
            slug = base_slug
            num = 1
            while PropertyContact.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)