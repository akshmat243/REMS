from .models import *
from .serializers import *
from MBP.views import ProtectedModelViewSet
from rest_framework.decorators import action

class TransactionViewSet(ProtectedModelViewSet):
    queryset = Transaction.objects.all().order_by('-timestamp')
    serializer_class = TransactionSerializer
    model_name = "Transaction"
    lookup_field = "slug"
    
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        qs = self.get_queryset()
        current_month = now().month
        return Response({
            'total_transactions': qs.count(),
            'total_amount': qs.aggregate(Sum('amount'))['amount__sum'] or 0,
            'this_month': qs.filter(timestamp__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0,
        })
    
    @action(detail=False, methods=['get'], url_path='monthly-revenue')
    def monthly_revenue(self, request):
        revenue = self.get_queryset().annotate(
            month=TruncMonth('timestamp')
        ).values('month').annotate(total=Sum('amount')).order_by('month')
        return Response(revenue)


class InvoiceViewSet(ProtectedModelViewSet):
    queryset = Invoice.objects.all().order_by('-issued_at')
    serializer_class = InvoiceSerializer
    model_name = "Invoice"
    lookup_field = "slug"


class ReceiptViewSet(ProtectedModelViewSet):
    queryset = Receipt.objects.all().order_by('-issued_date')
    serializer_class = ReceiptSerializer
    model_name = "Receipt"
    lookup_field = "slug"


class CommissionViewSet(ProtectedModelViewSet):
    queryset = Commission.objects.all().order_by('-date')
    serializer_class = CommissionSerializer
    model_name = "Commission"
    lookup_field = "slug"

class RentRecieptViewSet(ProtectedModelViewSet):
    queryset = RentReceipt.objects.all()
    serializer_class = RentReceiptSerializer
    model_name = "Commission"
    lookup_field = "slug"