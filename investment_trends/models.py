from django.db import models
from django.utils.text import slugify
import uuid

class PriceTrend(models.Model):
    area = models.CharField(max_length=100)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    trend_date = models.DateField()
    market_indicator = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.area}-{self.trend_date}-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.area} - {self.trend_date}"

class InvestmentOpportunity(models.Model):
    RISK_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    roi = models.DecimalField("Return on Investment (%)", max_digits=5, decimal_places=2)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
