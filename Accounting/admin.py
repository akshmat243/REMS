from django.contrib import admin
from .models import Transaction, Invoice, Receipt, Commission

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
