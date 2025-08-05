from .models import *
from .serializers import *
from MBP.views import ProtectedModelViewSet
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.decorators import action

class PropertyViewSet(ProtectedModelViewSet):
    queryset = Property.objects.all().order_by('-listed_on')
    serializer_class = PropertySerializer
    model_name = "Property"
    lookup_field = "slug"
    
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = self.get_queryset()
        return Response({
            'total_properties': qs.count(),
            'average_price': qs.aggregate(Avg('price'))['price__avg'] or 0,
            'average_area': qs.aggregate(Avg('area_sqft'))['area_sqft__avg'] or 0,
            'active_count': qs.filter(property_status='Active').count(),
        })

    @action(detail=False, methods=['get'], url_path='price-breakdown')
    def price_breakdown(self, request):
        qs = self.get_queryset()
        return Response({
            "below_20_lakh": qs.filter(price__lt=2000000).count(),
            "between_20_50_lakh": qs.filter(price__gte=2000000, price__lt=5000000).count(),
            "above_50_lakh": qs.filter(price__gte=5000000).count(),
        })

    @action(detail=False, methods=['get'], url_path='top-ai-recommended')
    def top_ai_recommended(self, request):
        properties = self.get_queryset().filter(ai_recommended_score__gte=0.8).order_by('-ai_recommended_score')[:10]
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)

class PropertyTypeViewSet(ProtectedModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    model_name = "PropertyType"
    lookup_field = "slug"


class PropertyImageViewSet(ProtectedModelViewSet):
    queryset = PropertyImage.objects.all().order_by('-uploaded_at')
    serializer_class = PropertyImageSerializer
    model_name = "PropertyImage"
    lookup_field = "slug"


class PropertyAmenityViewSet(ProtectedModelViewSet):
    queryset = PropertyAmenity.objects.all()
    serializer_class = PropertyAmenitySerializer
    model_name = "PropertyAmenity"
    lookup_field = "slug"


class PropertyDocumentViewSet(ProtectedModelViewSet):
    queryset = PropertyDocument.objects.all()
    serializer_class = PropertyDocumentSerializer
    model_name = "PropertyDocument"
    lookup_field = "slug"
    
    @action(detail=False, methods=['get'], url_path='verification-rate')
    def verification_rate(self, request):
        total = self.get_queryset().count()
        verified = self.get_queryset().filter(verified=True).count()
        rate = round((verified / total) * 100, 2) if total else 0
        return Response({
            "total_documents": total,
            "verified": verified,
            "verification_rate_percent": rate
        })


class PostedPropertyViewSet(ProtectedModelViewSet):
    queryset = PostedProperty.objects.all()
    serializer_class = PostedPropertySerializer
    model_name = "PostedProperty"
    lookup_field = "slug"


