from django.contrib import admin
from .models import Transaction, Invoice, Receipt, Commission, RentReceipt

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'timestamp']
    list_filter = ['transaction_type']
    search_fields = ['user__full_name']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'issued_at', 'status']
    list_filter = ['status']
    search_fields = ['user__full_name']

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'receipt_number', 'issued_date']
    search_fields = ['invoice__id', 'receipt_number']

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ['agent', 'amount', 'property', 'date']
    list_filter = ['date']
    search_fields = ['agent__full_name', 'property__title']

@admin.register(RentReceipt)
class RentReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "receipt_number",
        "tenant_name",
        "landlord_name",
        "rent_amount",
        "payment_date",
        "payment_method",
        "period",
        "created_at",
    )
    list_filter = ("period", "payment_method", "created_at")
    search_fields = ("receipt_number", "tenant_name", "landlord_name", "property_address")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Receipt Info", {"fields": ("receipt_number",)}),
        ("Tenant Details", {"fields": ("tenant_name", "tenant_address")}),
        ("Landlord Details", {"fields": ("landlord_name", "landlord_address")}),
        (
            "Property & Payment Details",
            {"fields": ("property_address", "rent_amount", "period", "payment_date", "payment_method")},
        ),
        ("Additional", {"fields": ("additional_notes",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )