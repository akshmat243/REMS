from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('properties', PropertyViewSet)
router.register('property-types', PropertyTypeViewSet)
router.register('property-images', PropertyImageViewSet)
router.register('property-amenities', PropertyAmenityViewSet)
router.register('property-documents', PropertyDocumentViewSet)
router.register('posted-properties', PostedPropertyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]


# GET /api/properties/stats/