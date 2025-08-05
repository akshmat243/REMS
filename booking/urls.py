from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('visits', VisitRequestViewSet)
router.register('appointments', AppointmentViewSet)
router.register('rent-agreements', RentAgreementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
