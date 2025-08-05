from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('transactions', TransactionViewSet)
router.register('invoices', InvoiceViewSet)
router.register('receipts', ReceiptViewSet)
router.register('commissions', CommissionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
