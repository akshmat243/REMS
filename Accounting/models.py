from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from property.models import Property
import uuid

User = get_user_model()

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Credit', 'Credit'),
        ('Debit', 'Debit'),
        ('Refund', 'Refund'),
        ('Commission', 'Commission'),
        ('Rent Payment', 'Rent Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"txn-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ₹{self.amount}"

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"invoice-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.id} - {self.user.username} - {self.status}"

class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=100)
    issued_date = models.DateField()
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ['invoice', 'receipt_number']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"receipt-{self.receipt_number}-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt #{self.receipt_number}"

class Commission(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commissions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"commission-{uuid.uuid4()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.agent.username} - Commission - ₹{self.amount}"
