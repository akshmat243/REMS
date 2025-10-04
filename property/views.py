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


class PropertyViewSet(ProtectedModelViewSet):
    queryset = Property.objects.all().order_by('-listed_on')
    serializer_class = PropertySerializer
    model_name = "Property"
    lookup_field = "slug"
    
    @action(detail=False, methods=["get"], url_path="search", permission_classes=[AllowAny])
    def search_properties(self, request):
        """
        Public API: Search properties by filters
        Example:
        /api/properties/search/?category=Sale&type=Apartment&status=Active&new_launch=true
        """
        category = request.GET.get("category")              
        property_type = request.GET.get("type")             
        property_status = request.GET.get("status")         
        furnishing = request.GET.get("furnishing")          
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        bedrooms = request.GET.get("bedrooms")
        location = request.GET.get("location")
        new_launch = request.GET.get("new_launch")          

        queryset = Property.objects.all()

        # --- Exact match filters ---
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

        # --- Fallback OR search ---
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

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
        Public API: Returns property counts, prices, and one image grouped by city.
        City name is extracted from `location` field.
        Example Response:
        [
            {
                "city": "Mumbai",
                "total_properties": 120,
                "min_price": 2500000,
                "max_price": 75000000,
                "avg_price": 4500000,
                "image": "http://127.0.0.1:8000/media/property_images/mumbai.jpg"
            }
        ]
        """

        properties = Property.objects.all()
        city_data = {}

        for prop in properties:
            # Extract city (last part of location, strip spaces)
            raw_location = prop.location or "Unknown"
            parts = raw_location.split(",")
            city = parts[-1].strip() if len(parts) > 1 else raw_location.strip()

            if city not in city_data:
                city_data[city] = {
                    "city": city,
                    "total_properties": 0,
                    "prices": [],
                    "image": None,
                }

            city_data[city]["total_properties"] += 1
            city_data[city]["prices"].append(float(prop.price))

            # Assign first image if not already set
            if not city_data[city]["image"]:
                first_image = prop.images.first()
                if first_image and first_image.image:
                    city_data[city]["image"] = request.build_absolute_uri(first_image.image.url)

        # Format response
        formatted_data = []
        for city, info in city_data.items():
            prices = info["prices"]
            formatted_data.append({
                "city": city,
                "total_properties": info["total_properties"],
                # "min_price": min(prices) if prices else None,
                # "max_price": max(prices) if prices else None,
                # "avg_price": round(sum(prices) / len(prices), 2) if prices else None,
                "image": info["image"]
            })

        return Response(formatted_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="top-video-properties", permission_classes=[AllowAny])
    def top_video_properties(self, request):
        """
        Public API: Returns top 5 properties that have videos
        """
        properties = (
            Property.objects.filter(videos__isnull=False)
            .distinct()
            .order_by("-listed_on")[:5]
        )
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
    
    @action(detail=False, methods=["get"], url_path="top-ai-properties", permission_classes=[AllowAny])
    def top_ai_properties(self, request):
        """
        Public API: Returns top 3 properties based on AI recommended score.
        Example Response:
        [
            {"id": 1, "title": "Luxury Villa", "ai_recommended_score": 0.95},
            {"id": 2, "title": "3BHK Apartment", "ai_recommended_score": 0.92},
            {"id": 3, "title": "Office Space", "ai_recommended_score": 0.90}
        ]
        """
        properties = (
            Property.objects.filter(property_status="Active", ai_recommended_score__isnull=False)
            .order_by("-ai_recommended_score")
        )
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="ai-properties", permission_classes=[AllowAny])
    def ai_properties(self, request):
        """
        Public API: Returns AI-ranked properties with optional filters.
        Query params:
        - limit: number of properties (default = 6)
        - category: Sale / Rent / Lease (optional)
        
        Example:
        GET /api/properties/ai-properties/?limit=6&category=Sale
        """
        limit = int(request.query_params.get("limit", 6))
        category = request.query_params.get("category", None)

        qs = Property.objects.filter(property_status="Active", ai_recommended_score__isnull=False)

        if category:
            qs = qs.filter(category=category)

        properties = qs.order_by("-ai_recommended_score")[:limit]
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


