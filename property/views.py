from .models import *
from .serializers import *
from MBP.views import ProtectedModelViewSet
from django.db.models import Avg, Count, Min, Max, Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.decorators import api_view
from .models import Property
from .serializers import PropertySerializer

from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def search_properties(request):
    """
    Search API
    Example: /api/properties/search/?category=Sale&type=Apartment&status=Active&new_launch=true
    """
    category = request.GET.get("category")              # Sale / Rent / Lease
    property_type = request.GET.get("type")             # e.g. Apartment, Villa
    property_status = request.GET.get("status")         # Active / Sold / Rented
    furnishing = request.GET.get("furnishing")          # Furnished / Unfurnished
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    bedrooms = request.GET.get("bedrooms")
    location = request.GET.get("location")
    new_launch = request.GET.get("new_launch")          # true / false

    queryset = Property.objects.all()

    # --- Step 1: Exact match when group of filters provided ---
    filters = {}
    if category:
        filters["category"] = category
    if property_type:
        filters["property_type__name__iexact"] = property_type
    if property_status:
        filters["property_status"] = property_status
    if furnishing:
        filters["furnishing"] = furnishing
    if bedrooms:
        filters["bedrooms"] = bedrooms
    if min_price and max_price:
        filters["price__gte"] = min_price
        filters["price__lte"] = max_price
    if location:
        filters["location__icontains"] = location
    if new_launch and new_launch.lower() == "true":
        filters["listed_on__gte"] = now() - timedelta(days=30)

    if filters:
        queryset = queryset.filter(**filters)

    print("SQL:", queryset.query)
    # --- Step 2: If nothing found, try OR-based fallback search ---
    if not queryset.exists() and filters:
        q = Q()
        if category:
            q |= Q(category=category)
        if property_type:
            q |= Q(property_type__name__iexact=property_type)
        if property_status:
            q |= Q(property_status=property_status)
        if furnishing:
            q |= Q(furnishing=furnishing)
        if bedrooms:
            q |= Q(bedrooms=bedrooms)
        if min_price and max_price:
            q |= Q(price__gte=min_price, price__lte=max_price)
        if location:
            q |= Q(location__icontains=location)
        if new_launch and new_launch.lower() == "true":
            q |= Q(listed_on__gte=now() - timedelta(days=30))

        queryset = Property.objects.filter(q)

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
    
    @action(detail=False, methods=["get"], url_path="stats/location", permission_classes=[AllowAny])
    def stats_location(self, request):
        """
        Public API: Returns property counts and price ranges grouped by city.
        Example Response:
        [
            {
                "city": "Mumbai",
                "total_properties": 120,
                "min_price": 2500000,
                "max_price": 75000000,
                "avg_price": 4500000
            }
        ]
        """
        data = (
            Property.objects
            .values("address__city")
            .annotate(
                total_properties=Count("id"),
            )
            .order_by("-total_properties")
        )
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="stats/property-type", permission_classes=[AllowAny])
    def stats_property_type(self, request):
        """
        Public API: Returns property counts grouped by property type.
        Example Response:
        [
            {"property_type": "Apartment", "total_properties": 120},
            {"property_type": "Villa", "total_properties": 45},
            {"property_type": "Commercial", "total_properties": 30}
        ]
        """
        data = (
            Property.objects
            .values("property_type__name")
            .annotate(total_properties=Count("id"))
            .order_by("-total_properties")
        )
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="top-properties", permission_classes=[AllowAny])
    def top_properties(self, request):
        """
        Public API: Returns top 3 latest active properties.
        Example Response:
        [
            {"id": 1, "title": "Luxury Villa", "price": "5000000.00"},
            {"id": 2, "title": "2BHK Apartment", "price": "2500000.00"},
            {"id": 3, "title": "Office Space", "price": "7500000.00"}
        ]
        """
        properties = (
            Property.objects.filter(property_status="Active")
            .order_by("-listed_on")[:3]
        )
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


