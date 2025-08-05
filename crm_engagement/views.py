from .models import *
from .serializers import *
from MBP.views import ProtectedModelViewSet
from rest_framework.decorators import action

class LeadViewSet(ProtectedModelViewSet):
    queryset = Lead.objects.all().order_by('-id')
    serializer_class = LeadSerializer
    model_name = "Lead"
    lookup_field = "slug"
    
    @action(detail=False, methods=['get'], url_path='conversion-rate')
    def conversion_rate(self, request):
        total = self.get_queryset().count()
        converted = self.get_queryset().filter(status__iexact="Converted").count()
        rate = round((converted / total) * 100, 2) if total else 0
        return Response({
            "total_leads": total,
            "converted": converted,
            "conversion_rate_percent": rate
        })


class InteractionLogViewSet(ProtectedModelViewSet):
    queryset = InteractionLog.objects.all().order_by('-date')
    serializer_class = InteractionLogSerializer
    model_name = "InteractionLog"
    lookup_field = "slug"


class NotificationViewSet(ProtectedModelViewSet):
    queryset = Notification.objects.all().order_by('-id')
    serializer_class = NotificationSerializer
    model_name = "Notification"
    lookup_field = "slug"


class WishlistViewSet(ProtectedModelViewSet):
    queryset = Wishlist.objects.all().order_by('-added_at')
    serializer_class = WishlistSerializer
    model_name = "Wishlist"
    lookup_field = "slug"


class PropertyComparisonViewSet(ProtectedModelViewSet):
    queryset = PropertyComparison.objects.all().order_by('-compared_at')
    serializer_class = PropertyComparisonSerializer
    model_name = "PropertyComparison"
    lookup_field = "slug"
