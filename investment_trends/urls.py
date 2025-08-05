from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('price-trends', PriceTrendViewSet)
router.register('opportunities', InvestmentOpportunityViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
