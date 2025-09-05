from .models import *
from .serializers import *
from MBP.views import ProtectedModelViewSet
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer

@api_view(["GET"])
def search_properties(request):
    """
    Search API
    Example: /api/properties/search/?category=Sale&type=Apartment&status=Active
    """
    category = request.GET.get("category")              # Sale / Rent / Lease
    property_type = request.GET.get("type")             # e.g. Apartment, Villa (FK name)
    property_status = request.GET.get("status")         # Active / Sold / Rented
    furnishing = request.GET.get("furnishing")          # Furnished / Unfurnished
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    bedrooms = request.GET.get("bedrooms")
    location = request.GET.get("location")

    queryset = Property.objects.all()

    # Apply filters
    if category:
        queryset = queryset.filter(category=category)

    if property_type:
        queryset = queryset.filter(property_type__name__iexact=property_type)

    if property_status:
        queryset = queryset.filter(property_status=property_status)

    if furnishing:
        queryset = queryset.filter(furnishing=furnishing)

    if min_price and max_price:
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

    if bedrooms:
        queryset = queryset.filter(bedrooms=bedrooms)

    if location:
        queryset = queryset.filter(location__icontains=location)

    serializer = PropertySerializer(queryset, many=True)
    return Response(serializer.data)


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


